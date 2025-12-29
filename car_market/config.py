import os
from datetime import timedelta

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'car-market-super-secret-key-2024'
    
    # PostgreSQL bağlantısı - ŞİFRENİ BURAYA YAZ
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'postgresql://postgres:postgres@localhost:5432/car_markt'
    
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Upload ayarları
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024
    UPLOAD_FOLDER = 'uploads'
    
    # Session ayarları
    PERMANENT_SESSION_LIFETIME = timedelta(days=7)
    
    # Pagination
    LISTINGS_PER_PAGE = 12
    MESSAGES_PER_PAGE = 10