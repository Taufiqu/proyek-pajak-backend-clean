# =========================================================================
# STAGE 1: Builder - Tempat kita menginstal semua yang berat
# =========================================================================
FROM python:3.11-slim AS builder

# 1. Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on

# 2. Instal dependensi sistem yang diperlukan untuk build
#    Menggunakan --no-install-recommends untuk menjaga ukuran tetap kecil
RUN apt-get update && apt-get install -y --no-install-recommends \
    poppler-utils \
    tesseract-ocr \
    git \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# 3. Buat dan aktifkan virtual environment
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# 4. Salin requirements dan instal dependensi Python ke dalam venv
COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

# 5. INI BAGIAN KUNCI: Paksa EasyOCR mengunduh modelnya di sini
#    Folder /root/.EasyOCR/ akan dibuat dan diisi di dalam stage ini.
RUN python -c "import easyocr; reader = easyocr.Reader(['id', 'en'], gpu=False, model_storage_directory='/opt/easyocr_models')"

# =========================================================================
# STAGE 2: Final - Image akhir yang bersih dan kecil
# =========================================================================
FROM python:3.11-slim AS final

# 1. Buat user non-root untuk keamanan
RUN useradd --create-home --shell /bin/bash appuser
USER appuser
WORKDIR /home/appuser/app

# 2. Instal dependensi sistem yang diperlukan untuk RUNTIME saja
RUN apt-get update && apt-get install -y --no-install-recommends \
    poppler-utils \
    tesseract-ocr \
    libgl1-mesa-glx \
    libglib2.0-0 \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# 3. Salin virtual environment dari builder stage
COPY --chown=appuser:appuser --from=builder /opt/venv /opt/venv

# 4. Salin model EasyOCR yang sudah di-download dari builder stage
#    Menyalin dari lokasi custom yang kita definisikan di atas
COPY --chown=appuser:appuser --from=builder /opt/easyocr_models /home/appuser/.EasyOCR

# 5. Salin kode aplikasi Anda
COPY --chown=appuser:appuser . .

# 6. Atur path ke venv, atur path model easyocr, dan jalankan aplikasi
ENV PATH="/opt/venv/bin:$PATH"
# Beritahu easyocr di mana menemukan model yang sudah kita salin
ENV EASYOCR_MODULE_PATH=/home/appuser/.EasyOCR

# Pastikan gunicorn ada di requirements.txt Anda
EXPOSE 5000
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "2", "--timeout", "120", "app:app"]