from flask import Blueprint, render_template, request, send_from_directory, current_app
import os
from app.models import Listing
from app.forms import SearchForm
from app.search import advanced_search  # search.py fonksiyonunu içeri aktar

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
@main_bp.route('/home')
def index():
    featured_listings = Listing.query.filter_by(is_active=True)\
        .order_by(Listing.created_at.desc())\
        .limit(8).all()
    
    return render_template('listings/index.html', 
                         featured_listings=featured_listings)

@main_bp.route('/about')
def about():
    return render_template('about.html')

@main_bp.route('/contact')
def contact():
    return render_template('contact.html')

@main_bp.route('/search')
def search():
    form = SearchForm()
    page = request.args.get('page', 1, type=int)
    
    # Tüm filtreleme ve sıralama işini search.py içindeki bu fonksiyon yapar
    query = advanced_search()
    
    # Sayfalamayı burada yapıyoruz
    listings = query.paginate(page=page, per_page=12, error_out=False)
    
    return render_template('listings/search.html', 
                         listings=listings, 
                         form=form,
                         search_query=request.args.get('query', ''))

@main_bp.route('/uploads/<path:filename>')
def uploaded_file(filename):
    upload_root = os.path.abspath(os.path.join(current_app.root_path, os.pardir, current_app.config.get('UPLOAD_FOLDER', 'uploads')))
    return send_from_directory(upload_root, filename)