from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed, MultipleFileField
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField, FloatField, IntegerField, SelectField, SelectMultipleField
from wtforms.validators import DataRequired, Email, EqualTo, Length, ValidationError, NumberRange, Optional
from datetime import datetime
from app.models import User

class RegistrationForm(FlaskForm):
    username = StringField('Kullanıcı Adı', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Şifre', validators=[DataRequired()])
    confirm_password = PasswordField('Şifre Tekrar', validators=[DataRequired(), EqualTo('password')])
    user_type = SelectField('Hesap Türü', choices=[('buyer', 'Alıcı'), ('seller', 'Satıcı')], validators=[DataRequired()])
    phone = StringField('Telefon', validators=[Optional()])
    location = StringField('Konum', validators=[Optional()])
    submit = SubmitField('Kayıt Ol')
    
    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Bu kullanıcı adı zaten alınmış.')
    
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Bu email adresi zaten kayıtlı.')

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Şifre', validators=[DataRequired()])
    remember = BooleanField('Beni Hatırla')
    submit = SubmitField('Giriş Yap')

class ProfileForm(FlaskForm):
    username = StringField('Kullanıcı Adı', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    phone = StringField('Telefon')
    location = StringField('Konum')
    about_me = TextAreaField('Hakkımda')
    profile_picture = FileField('Profil Resmi', validators=[FileAllowed(['jpg', 'jpeg', 'png'])])
    submit = SubmitField('Profili Güncelle')

class ListingForm(FlaskForm):
    title = StringField('İlan Başlığı', validators=[DataRequired(), Length(max=200)])
    description = TextAreaField('Açıklama', validators=[DataRequired()])
    price = FloatField('Fiyat', validators=[DataRequired(), NumberRange(min=0)])
    brand = SelectField('Marka', choices=[
        ('', 'Marka Seçiniz'),
        ('Audi', 'Audi'), ('BMW', 'BMW'), ('Mercedes', 'Mercedes'),
        ('Volkswagen', 'Volkswagen'), ('Ford', 'Ford'), ('Renault', 'Renault'),
        ('Fiat', 'Fiat'), ('Toyota', 'Toyota'), ('Honda', 'Honda'),
        ('Hyundai', 'Hyundai'), ('Opel', 'Opel'), ('Peugeot', 'Peugeot'),
        ('Citroen', 'Citroen'), ('Nissan', 'Nissan'), ('Mazda', 'Mazda'),
        ('Volvo', 'Volvo'), ('Skoda', 'Skoda'), ('Seat', 'Seat')
    ], validators=[DataRequired()])
    model = StringField('Model', validators=[DataRequired()])
    year = IntegerField('Yıl', validators=[DataRequired(), NumberRange(min=1950, max=datetime.utcnow().year)])
    km = IntegerField('Kilometre', validators=[DataRequired(), NumberRange(min=0)])
    fuel_type = SelectField('Yakıt Türü', choices=[
        ('', 'Seçiniz'), ('Benzin', 'Benzin'), ('Dizel', 'Dizel'), 
        ('Elektrik', 'Elektrik'), ('Hibrit', 'Hibrit'), ('LPG', 'LPG')
    ], validators=[DataRequired()])
    gear_type = SelectField('Vites Türü', choices=[
        ('', 'Seçiniz'), ('Manuel', 'Manuel'), ('Otomatik', 'Otomatik'),
        ('Yarı Otomatik', 'Yarı Otomatik')
    ], validators=[DataRequired()])
    color = StringField('Renk')
    location = StringField('Konum', validators=[DataRequired()])
    images = MultipleFileField('Araç Resimleri (En fazla 5 resim)', validators=[
        FileAllowed(['jpg', 'jpeg', 'png'], 'Sadece JPG, JPEG ve PNG dosyaları yükleyebilirsiniz.')
    ])
    submit = SubmitField('İlanı Oluştur')

class MessageForm(FlaskForm):
    subject = StringField('Konu', validators=[DataRequired(), Length(max=200)])
    body = TextAreaField('Mesaj', validators=[DataRequired()])
    submit = SubmitField('Mesaj Gönder')

class SearchForm(FlaskForm):
    query = StringField('Arama')
    brand = SelectField('Marka', choices=[('', 'Tüm Markalar')] + [
        ('Audi', 'Audi'), ('BMW', 'BMW'), ('Mercedes', 'Mercedes'),
        ('Volkswagen', 'Volkswagen'), ('Ford', 'Ford'), ('Renault', 'Renault'),
        ('Fiat', 'Fiat'), ('Toyota', 'Toyota'), ('Honda', 'Honda'),
        ('Hyundai', 'Hyundai'), ('Opel', 'Opel'), ('Peugeot', 'Peugeot'),
        ('Citroen', 'Citroen'), ('Nissan', 'Nissan'), ('Mazda', 'Mazda'),
        ('Volvo', 'Volvo'), ('Skoda', 'Skoda'), ('Seat', 'Seat')
    ])
    min_price = IntegerField('Min Fiyat', validators=[Optional(), NumberRange(min=0)])
    max_price = IntegerField('Max Fiyat', validators=[Optional(), NumberRange(min=0)])
    min_year = IntegerField('Min Yıl', validators=[Optional(), NumberRange(min=1950, max=2024)])
    max_year = IntegerField('Max Yıl', validators=[Optional(), NumberRange(min=1950, max=2024)])
    fuel_type = SelectField('Yakıt Türü', choices=[('', 'Tüm Yakıt Türleri')] + [
        ('Benzin', 'Benzin'), ('Dizel', 'Dizel'), ('Elektrik', 'Elektrik'),
        ('Hibrit', 'Hibrit'), ('LPG', 'LPG')
    ])
    gear_type = SelectField('Vites Türü', choices=[('', 'Tüm Vites Türleri')] + [
        ('Manuel', 'Manuel'), ('Otomatik', 'Otomatik'), ('Yarı Otomatik', 'Yarı Otomatik')
    ])
    location = StringField('Konum')
    submit = SubmitField('Ara')