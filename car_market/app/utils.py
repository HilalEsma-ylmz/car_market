import os
from werkzeug.utils import secure_filename
from PIL import Image
import secrets
from flask import current_app

def save_image(image_file, folder):
    if image_file:
        # Güvenli dosya adı oluştur
        random_hex = secrets.token_hex(8)
        _, f_ext = os.path.splitext(image_file.filename)
        filename = random_hex + f_ext.lower()
        
        # Proje kökünde uploads klasörünü kullan
        upload_root = os.path.abspath(os.path.join(current_app.root_path, os.pardir, current_app.config.get('UPLOAD_FOLDER', 'uploads')))
        upload_path = os.path.join(upload_root, folder)
        os.makedirs(upload_path, exist_ok=True)
        
        filepath = os.path.join(upload_path, filename)
        
        try:
            # Resmi optimize et ve kaydet
            output_size = (800, 600)
            i = Image.open(image_file)
            
            # PNG formatını RGB'ye çevir (JPEG için)
            if i.mode in ('RGBA', 'LA', 'P'):
                i = i.convert('RGB')
            
            i.thumbnail(output_size, Image.Resampling.LANCZOS)
            i.save(filepath, optimize=True, quality=85)
            
            return filename
        except Exception as e:
            print(f"Resim kaydetme hatası: {e}")
            return None
    
    return None

def delete_image(filename, folder):
    if filename:
        upload_root = os.path.abspath(os.path.join(current_app.root_path, os.pardir, current_app.config.get('UPLOAD_FOLDER', 'uploads')))
        filepath = os.path.join(upload_root, folder, filename)
        if os.path.exists(filepath):
            try:
                os.remove(filepath)
                return True
            except Exception as e:
                print(f"Resim silme hatası: {e}")
                return False
    return False

def allowed_file(filename, allowed_extensions=None):
    if allowed_extensions is None:
        allowed_extensions = {'png', 'jpg', 'jpeg', 'gif'}
    
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in allowed_extensions