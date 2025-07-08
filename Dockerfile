# =========================================================================
# STAGE 1: Builder - Tempat kita menginstal semua yang berat
# =========================================================================
FROM python:3.11-slim AS builder

# 1. Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on

# 2. Instal dependensi sistem yang diperlukan untuk build
# 🔥 PERUBAHAN DI SINI: Menambahkan library yang dibutuhkan OpenCV
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    poppler-utils \
    tesseract-ocr \
    git \
    libgl1-mesa-glx \
    libglib2.0-0 \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# 3. Buat dan aktifkan virtual environment
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# 4. Salin requirements dan instal dependensi Python ke dalam venv
COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

# 5. Paksa EasyOCR mengunduh modelnya di sini
RUN python -c "import easyocr; reader = easyocr.Reader(['id', 'en'], gpu=False, model_storage_directory='/opt/easyocr_models')"

# =========================================================================
# STAGE 2: Final - Image akhir yang bersih dan kecil
# =========================================================================
FROM python:3.11-slim AS final

# Instal dependensi sistem yang diperlukan untuk RUNTIME saja
RUN apt-get update && apt-get install -y --no-install-recommends \
    poppler-utils \
    tesseract-ocr \
    libgl1-mesa-glx \
    libglib2.0-0 \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Buat user non-root dan direktori kerja
RUN useradd --create-home --shell /bin/bash appuser
WORKDIR /home/appuser/app

# Salin virtual environment dari builder stage
COPY --chown=appuser:appuser --from=builder /opt/venv /opt/venv

# Salin model EasyOCR yang sudah di-download dari builder stage
COPY --chown=appuser:appuser --from=builder /opt/easyocr_models /home/appuser/.EasyOCR

# Salin kode aplikasi Anda
COPY --chown=appuser:appuser . .

# Ganti ke user non-root untuk menjalankan aplikasi (lebih aman)
USER appuser

# Atur path ke venv, atur path model easyocr, dan jalankan aplikasi
ENV PATH="/opt/venv/bin:$PATH"
ENV EASYOCR_MODULE_PATH=/home/appuser/.EasyOCR

# Pastikan gunicorn ada di requirements.txt Anda
EXPOSE 5000
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "2", "--timeout", "120", "app:app"]