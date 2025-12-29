from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app import db
from app.models import User, Listing, Favorite, Message
from app.forms import ProfileForm
from app.utils import save_image

user_bp = Blueprint('user', __name__)

@user_bp.route('/dashboard')
@login_required
def dashboard():
    if current_user.user_type == 'seller':
        listings = Listing.query.filter_by(seller_id=current_user.id)\
            .order_by(Listing.created_at.desc())\
            .limit(5).all()
        total_listings = Listing.query.filter_by(seller_id=current_user.id).count()
        active_listings = Listing.query.filter_by(seller_id=current_user.id, is_active=True).count()
        
        return render_template('user/dashboard.html', 
                             listings=listings,
                             total_listings=total_listings,
                             active_listings=active_listings)
    else:
        favorites = Favorite.query.filter_by(user_id=current_user.id)\
            .order_by(Favorite.created_at.desc())\
            .limit(5).all()
        total_favorites = Favorite.query.filter_by(user_id=current_user.id).count()
        unread_messages = Message.query.filter_by(receiver_id=current_user.id, is_read=False).count()
        
        return render_template('user/dashboard.html',
                             favorites=favorites,
                             total_favorites=total_favorites,
                             unread_messages=unread_messages)

@user_bp.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    form = ProfileForm()
    
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.email = form.email.data
        current_user.phone = form.phone.data
        current_user.location = form.location.data
        current_user.about_me = form.about_me.data
        
        if form.profile_picture.data:
            filename = save_image(form.profile_picture.data, 'profile_pictures')
            if filename:
                current_user.profile_picture = filename
        
        db.session.commit()
        flash('Profiliniz başarıyla güncellendi!', 'success')
        return redirect(url_for('user.profile'))
    
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
        form.phone.data = current_user.phone
        form.location.data = current_user.location
        form.about_me.data = current_user.about_me
    
    return render_template('user/profile.html', form=form)

@user_bp.route('/favorites')
@login_required
def favorites():
    page = request.args.get('page', 1, type=int)
    favorites = Favorite.query.filter_by(user_id=current_user.id)\
        .order_by(Favorite.created_at.desc())\
        .paginate(page=page, per_page=12, error_out=False)
    
    return render_template('user/favorites.html', favorites=favorites)