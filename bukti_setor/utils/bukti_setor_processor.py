import time
import os
from PIL import Image
import numpy as np
import cv2
from pdf2image import convert_from_path
from flask import current_app
from .ocr_engine import process_with_easyocr
from .spellcheck import correct_spelling
from shared_utils.text_utils import clean_transaction_value, fuzzy_month_match
from shared_utils.file_utils import allowed_file, is_valid_image, is_image_file
from shared_utils.image_utils import preprocess_for_easyocr
from .helpers import simpan_preview_image
from .parsing.tanggal import parse_tanggal
from .parsing.jumlah import parse_jumlah
from .parsing.kode_setor import parse_kode_setor

def _extract_data_from_image(pil_image, upload_folder, page_num=1, original_filename="bukti_setor"):
    start_total = time.time()
    
    current_app.logger.debug(f"[🔥] Mulai proses halaman {page_num} dari {original_filename}")

    # ✅ FIXED: Lengkapi semua argumen
    preview_filename = simpan_preview_image(
        pil_image=pil_image,
        upload_folder=upload_folder,
        page_num=page_num,
        original_filename=original_filename
    )
    
    current_app.logger.debug(f"[🎯] Preview filename hasil: {preview_filename}")
    current_app.logger.debug(f"[📁] Upload folder: {upload_folder}")


    if not preview_filename:
        raise ValueError("Gagal menyimpan preview image.")
    # ✅ FIXED: Pastikan konversi ke OpenCV format
    img_cv = cv2.cvtColor(np.array(pil_image), cv2.COLOR_RGB2BGR)

    # Resize jika terlalu besar
    MAX_WIDTH = 1000
    if img_cv.shape[1] > MAX_WIDTH:
        ratio = MAX_WIDTH / img_cv.shape[1]
        img_cv = cv2.resize(img_cv, None, fx=ratio, fy=ratio, interpolation=cv2.INTER_AREA)

    processed_img = preprocess_for_easyocr(img_cv)
    
    # Get OCR results using lazy-loaded EasyOCR with error handling
    try:
        ocr_results = process_with_easyocr(processed_img)
        
        if not ocr_results:
            current_app.logger.warning(f"[⚠️ PERINGATAN] Tidak ada hasil OCR untuk halaman {page_num}")
            return {
                "kode_setor": "",
                "jumlah": "",
                "tanggal": None,
                "preview_filename": preview_filename,
                "warning": "Tidak ada teks terdeteksi"
            }
            
        # Debug EasyOCR input
        debug_text = " ".join([res[1] for res in ocr_results if len(res[1].strip()) >= 3])
        print(f"[🤖 DEBUG OCR-EasyOCR Input] Halaman {page_num} ------------")
        print(debug_text[:500] + "..." if len(debug_text) > 500 else debug_text)
        print("--------------------------------------------")

        cleaned_ocr = [res[1].strip().lower() for res in ocr_results if len(res[1].strip()) >= 3]
        
        # Only apply spell correction to significant text blocks
        all_text_blocks = []
        for text in cleaned_ocr:
            if len(text) > 2:  # Only spell-check text longer than 2 characters
                corrected = correct_spelling(text)
                all_text_blocks.append(corrected)
            else:
                all_text_blocks.append(text)
        
        full_text_str = " ".join(all_text_blocks)
        
    except Exception as e:
        current_app.logger.error(f"[❌ ERROR OCR] Halaman {page_num}: {str(e)}")
        return {
            "kode_setor": "",
            "jumlah": "",
            "tanggal": None,
            "preview_filename": preview_filename,
            "error": f"Error OCR: {str(e)}"
        }

    kode_setor = parse_kode_setor(full_text_str)
    tanggal_obj = parse_tanggal(all_text_blocks)
    jumlah = parse_jumlah(all_text_blocks)

    return {
        "kode_setor": kode_setor,
        "jumlah": jumlah,
        "tanggal": tanggal_obj.isoformat() if tanggal_obj else None,
        "preview_filename": preview_filename
    }

def extract_bukti_setor_data(filepath, poppler_path):
    upload_folder = current_app.config['UPLOAD_FOLDER']
    
    # OCR akan di-initialize secara lazy saat process_with_easyocr dipanggil
    list_of_results = []
    filename_only = os.path.basename(filepath)

    if filepath.lower().endswith('.pdf'):
        all_pages_as_images = convert_from_path(filepath, poppler_path=poppler_path)
        for i, page_image in enumerate(all_pages_as_images):
            result_data = _extract_data_from_image(
                pil_image=page_image,
                upload_folder=upload_folder,
                page_num=i + 1,
                original_filename=filename_only
            )
            list_of_results.append(result_data)
    else:
        pil_image = Image.open(filepath)
        result_data = _extract_data_from_image(
            pil_image=pil_image,
            upload_folder=upload_folder,
            page_num=1,
            original_filename=filename_only
        )
        list_of_results.append(result_data)

    return list_of_results
def extract_bukti_setor_from_request(request):
    if "file" not in request.files:
        raise ValueError("File tidak ditemukan dalam request.")

    file = request.files["file"]
    if not allowed_file(file.filename):
        raise ValueError("File tidak didukung. Gunakan PDF atau gambar.")
    
    current_app.logger.debug(f"[📥] File diterima: {file.filename}")
    current_app.logger.debug(f"[📁] Upload folder: {upload_folder}")

    if file.filename.lower().endswith(('.jpg', '.jpeg', '.png')):
        if not is_valid_image(file):
            raise ValueError("File gambar tidak valid.")
    elif not is_image_file(file.filename):
        raise ValueError("File harus berupa gambar atau PDF.")

    upload_folder = current_app.config['UPLOAD_FOLDER']
    filepath = os.path.join(upload_folder, file.filename)
    file.save(filepath)

    poppler_path = current_app.config.get('POPPLER_PATH', None)
    if not poppler_path:
        raise ValueError("Path Poppler tidak ditemukan dalam konfigurasi aplikasi.")

    return extract_bukti_setor_data(filepath, poppler_path)