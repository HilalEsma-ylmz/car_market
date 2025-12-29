from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify, current_app
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
import os
from app import db
from app.models import Listing, ListingImage, Favorite, Message
from app.forms import ListingForm
from app.utils import save_image, delete_image

listings_bp = Blueprint('listings', __name__)

@listings_bp.route('/listings')
def listings():
    page = request.args.get('page', 1, type=int)
    listings = Listing.query.filter_by(is_active=True)\
        .order_by(Listing.created_at.desc())\
        .paginate(page=page, per_page=12, error_out=False)
    
    return render_template('listings/index.html', listings=listings)

@listings_bp.route('/listing/<int:listing_id>')
def listing_detail(listing_id):
    listing = Listing.query.get_or_404(listing_id)
    
    # Görüntülenme sayısını artır
    listing.view_count += 1
    db.session.commit()
    
    return render_template('listings/detail.html', listing=listing)

@listings_bp.route('/create_listing', methods=['GET', 'POST'])
@login_required
def create_listing():
    if current_user.user_type != 'seller':
        flash('İlan oluşturmak için satıcı hesabınız olmalıdır.', 'warning')
        return redirect(url_for('main.index'))
    
    form = ListingForm()
    if form.validate_on_submit():
        listing = Listing(
            title=form.title.data,
            description=form.description.data,
            price=form.price.data,
            brand=form.brand.data,
            model=form.model.data,
            year=form.year.data,
            km=form.km.data,
            fuel_type=form.fuel_type.data,
            gear_type=form.gear_type.data,
            color=form.color.data,
            location=form.location.data,
            seller_id=current_user.id
        )
        
        db.session.add(listing)
        db.session.commit()
        
        # Resimleri kaydet (en fazla 5 adet)
        if form.images.data:
            files = [f for f in form.images.data if f]
            for i, image_file in enumerate(files[:10]):
                filename = save_image(image_file, 'car_images')
                if filename:
                    listing_image = ListingImage(
                        filename=filename,
                        is_primary=(i == 0),
                        listing_id=listing.id
                    )
                    db.session.add(listing_image)
        
        db.session.commit()
        flash('İlanınız başarıyla oluşturuldu!', 'success')
        return redirect(url_for('listings.listing_detail', listing_id=listing.id))
    
    # POST olup doğrulama başarısızsa kullanıcıya hata göster
    if form.is_submitted() and not form.validate():
        for field, errors in form.errors.items():
            for err in errors:
                flash(f"{getattr(form, field).label.text}: {err}", 'danger')

    return render_template('listings/create.html', form=form)

@listings_bp.route('/favorite/<int:listing_id>', methods=['POST'])
@login_required
def toggle_favorite(listing_id):
    listing = Listing.query.get_or_404(listing_id)
    if listing.seller_id == current_user.id:
        return jsonify({'status': 'error', 'message': 'Kendi ilanınızı favorilere ekleyemezsiniz.'}), 400
    favorite = Favorite.query.filter_by(
        user_id=current_user.id, 
        listing_id=listing_id
    ).first()
    
    if favorite:
        db.session.delete(favorite)
        db.session.commit()
        return jsonify({'status': 'removed', 'message': 'Favorilerden kaldırıldı'})
    else:
        favorite = Favorite(user_id=current_user.id, listing_id=listing_id)
        db.session.add(favorite)
        db.session.commit()
        return jsonify({'status': 'added', 'message': 'Favorilere eklendi'})

@listings_bp.route('/my_listings')
@login_required
def my_listings():
    page = request.args.get('page', 1, type=int)
    listings = Listing.query.filter_by(seller_id=current_user.id)\
        .order_by(Listing.created_at.desc())\
        .paginate(page=page, per_page=10, error_out=False)
    
    return render_template('listings/my_listings.html', listings=listings)

@listings_bp.route('/edit_listing/<int:listing_id>', methods=['GET', 'POST'])
@login_required
def edit_listing(listing_id):
    listing = Listing.query.get_or_404(listing_id)
    
    if listing.seller_id != current_user.id:
        flash('Bu ilanı düzenleme yetkiniz yok.', 'danger')
        return redirect(url_for('main.index'))
    
    form = ListingForm()
    if form.validate_on_submit():
        listing.title = form.title.data
        listing.description = form.description.data
        listing.price = form.price.data
        listing.brand = form.brand.data
        listing.model = form.model.data
        listing.year = form.year.data
        listing.km = form.km.data
        listing.fuel_type = form.fuel_type.data
        listing.gear_type = form.gear_type.data
        listing.color = form.color.data
        listing.location = form.location.data
        
        db.session.commit()
        # Yeni resimleri ekle
        if form.images.data:
            files = [f for f in form.images.data if f]
            for i, image_file in enumerate(files[:10]):
                filename = save_image(image_file, 'car_images')
                if filename:
                    listing_image = ListingImage(
                        filename=filename,
                        is_primary=(len(listing.images) == 0 and i == 0),
                        listing_id=listing.id
                    )
                    db.session.add(listing_image)
        db.session.commit()
        flash('İlanınız başarıyla güncellendi!', 'success')
        return redirect(url_for('listings.edit_listing', listing_id=listing.id))
    
    elif request.method == 'GET':
        form.title.data = listing.title
        form.description.data = listing.description
        form.price.data = listing.price
        form.brand.data = listing.brand
        form.model.data = listing.model
        form.year.data = listing.year
        form.km.data = listing.km
        form.fuel_type.data = listing.fuel_type
        form.gear_type.data = listing.gear_type
        form.color.data = listing.color
        form.location.data = listing.location
    
    return render_template('listings/edit.html', form=form, listing=listing)

@listings_bp.route('/delete_image/<int:image_id>', methods=['POST'])
@login_required
def delete_listing_image(image_id):
    image = ListingImage.query.get_or_404(image_id)
    listing = Listing.query.get_or_404(image.listing_id)
    if listing.seller_id != current_user.id:
        flash('Bu işlem için yetkiniz yok.', 'danger')
        return redirect(url_for('main.index'))
    # Fiziksel dosyayı sil
    delete_image(image.filename, 'car_images')
    db.session.delete(image)
    db.session.commit()
    flash('Görsel silindi.', 'success')
    return redirect(url_for('listings.edit_listing', listing_id=listing.id))

@listings_bp.route('/delete_listing/<int:listing_id>', methods=['POST'])
@login_required
def delete_listing(listing_id):
    listing = Listing.query.get_or_404(listing_id)
    if listing.seller_id != current_user.id:
        flash('Bu ilanı silme yetkiniz yok.', 'danger')
        return redirect(url_for('main.index'))

    # İlana ait mesajlar ve favoriler
    Favorite.query.filter_by(listing_id=listing.id).delete()
    Message.query.filter_by(listing_id=listing.id).delete()

    # Görselleri sil (dosya + kayıt)
    for img in list(listing.images):
        delete_image(img.filename, 'car_images')
        db.session.delete(img)

    db.session.delete(listing)
    db.session.commit()
    flash('İlan başarıyla silindi.', 'success')
    return redirect(url_for('listings.my_listings'))