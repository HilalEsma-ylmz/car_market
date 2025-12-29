from flask import request
from app.models import Listing

def advanced_search():
    query = Listing.query.filter_by(is_active=True)
    
    # Arama sorgusu
    search_query = request.args.get('query', '')
    if search_query:
        query = query.filter(
            Listing.title.ilike(f'%{search_query}%') |
            Listing.description.ilike(f'%{search_query}%') |
            Listing.brand.ilike(f'%{search_query}%') |
            Listing.model.ilike(f'%{search_query}%')
        )
    
    # Filtreler (Marka, Fiyat, Yıl, Yakıt, Vites, Konum)
    brand = request.args.get('brand', '')
    if brand:
        query = query.filter(Listing.brand == brand)
    
    min_price = request.args.get('min_price', type=float)
    max_price = request.args.get('max_price', type=float)
    if min_price is not None:
        query = query.filter(Listing.price >= min_price)
    if max_price is not None:
        query = query.filter(Listing.price <= max_price)
    
    min_year = request.args.get('min_year', type=int)
    max_year = request.args.get('max_year', type=int)
    if min_year is not None:
        query = query.filter(Listing.year >= min_year)
    if max_year is not None:
        query = query.filter(Listing.year <= max_year)
    
    fuel_type = request.args.get('fuel_type', '')
    if fuel_type:
        query = query.filter(Listing.fuel_type == fuel_type)
    
    gear_type = request.args.get('gear_type', '')
    if gear_type:
        query = query.filter(Listing.gear_type == gear_type)
    
    location = request.args.get('location', '')
    if location:
        query = query.filter(Listing.location.ilike(f'%{location}%'))
    
    # Sıralama Mantığı
    sort_by = request.args.get('sort_by', 'created_at')
    sort_order = request.args.get('sort_order', 'desc')
    
    if sort_by == 'price':
        query = query.order_by(Listing.price.asc() if sort_order == 'asc' else Listing.price.desc())
    elif sort_by == 'year':
        query = query.order_by(Listing.year.asc() if sort_order == 'asc' else Listing.year.desc())
    elif sort_by == 'km':
        query = query.order_by(Listing.km.asc() if sort_order == 'asc' else Listing.km.desc())
    else:
        query = query.order_by(Listing.created_at.asc() if sort_order == 'asc' else Listing.created_at.desc())
    
    return query