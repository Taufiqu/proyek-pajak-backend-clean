# File: backend/config.py

import os
from dotenv import load_dotenv

# Muat variabel dari file .env
load_dotenv()

class Config:
    """Konfigurasi utama aplikasi Flask."""

    # Mengambil URI database dari environment variable, atau menggunakan default jika tidak ada
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "sqlite:///default.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Menambahkan konfigurasi untuk SSL connection (dibutuhkan untuk Supabase)
    SQLALCHEMY_ENGINE_OPTIONS = {
        'pool_pre_ping': True,
        'pool_recycle': 300,
        'connect_args': {
            'sslmode': 'require'
        }
    }

    # Mengambil path Poppler dari environment variable
    POPPLER_PATH = os.getenv("POPPLER_PATH")
    
    print("🔍 Database URL:", os.getenv("DATABASE_URL"))
    print("📦 POPPLER PATH:", os.getenv("POPPLER_PATH"))
    
    # Pengaturan folder upload
    UPLOAD_FOLDER = "uploads"
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)
