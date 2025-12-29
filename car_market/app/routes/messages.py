from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify
from flask_login import login_required, current_user
from app import db
from app.models import Message, User, Listing
from app.forms import MessageForm

messages_bp = Blueprint('messages', __name__)

@messages_bp.route('/inbox')
@login_required
def inbox():
    page = request.args.get('page', 1, type=int)
    messages = Message.query.filter_by(receiver_id=current_user.id)\
        .order_by(Message.created_at.desc())\
        .paginate(page=page, per_page=10, error_out=False)
    
    return render_template('messages/inbox.html', messages=messages)

@messages_bp.route('/sent')
@login_required
def sent():
    page = request.args.get('page', 1, type=int)
    messages = Message.query.filter_by(sender_id=current_user.id)\
        .order_by(Message.created_at.desc())\
        .paginate(page=page, per_page=10, error_out=False)
    
    return render_template('messages/sent.html', messages=messages)

@messages_bp.route('/message/<int:message_id>')
@login_required
def view_message(message_id):
    message = Message.query.get_or_404(message_id)
    
    if message.receiver_id != current_user.id and message.sender_id != current_user.id:
        flash('Bu mesajı görüntüleme yetkiniz yok.', 'danger')
        return redirect(url_for('messages.inbox'))
    
    if message.receiver_id == current_user.id and not message.is_read:
        message.is_read = True
        db.session.commit()
    
    return render_template('messages/conversation.html', message=message)

@messages_bp.route('/send_message/<int:listing_id>', methods=['GET', 'POST'])
@login_required
def send_message(listing_id):
    listing = Listing.query.get_or_404(listing_id)
    
    if listing.seller_id == current_user.id:
        flash('Kendi ilanınıza mesaj gönderemezsiniz.', 'warning')
        return redirect(url_for('listings.listing_detail', listing_id=listing_id))
    
    form = MessageForm()
    if form.validate_on_submit():
        message = Message(
            subject=form.subject.data,
            body=form.body.data,
            sender_id=current_user.id,
            receiver_id=listing.seller_id,
            listing_id=listing_id
        )
        
        db.session.add(message)
        db.session.commit()
        
        flash('Mesajınız gönderildi!', 'success')
        return redirect(url_for('listings.listing_detail', listing_id=listing_id))
    
    form.subject.data = f"Soru: {listing.title}"
    
    return render_template('messages/send.html', form=form, listing=listing)

@messages_bp.route('/reply_message/<int:message_id>', methods=['GET', 'POST'])
@login_required
def reply_message(message_id):
    original_message = Message.query.get_or_404(message_id)
    
    if original_message.sender_id != current_user.id and original_message.receiver_id != current_user.id:
        flash('Bu mesaja cevap verme yetkiniz yok.', 'danger')
        return redirect(url_for('messages.inbox'))
    
    form = MessageForm()
    
    if form.validate_on_submit():
        reply = Message(
            subject=f"Re: {original_message.subject}",
            body=form.body.data,
            sender_id=current_user.id,
            receiver_id=original_message.sender_id if current_user.id == original_message.receiver_id else original_message.receiver_id,
            listing_id=original_message.listing_id
        )
        
        db.session.add(reply)
        db.session.commit()
        
        flash('Cevabınız gönderildi!', 'success')
        return redirect(url_for('messages.inbox'))
    
    form.subject.data = f"Re: {original_message.subject}"
    
    return render_template('messages/send.html', form=form, original_message=original_message)