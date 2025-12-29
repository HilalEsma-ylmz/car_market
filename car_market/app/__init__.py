from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate

db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.login_message_category = 'info'

def create_app(config_class=None):
    app = Flask(__name__)
    
    # Config'i proje ana dizininden import et
    if config_class is None:
        from config import Config
        config_class = Config
    
    app.config.from_object(config_class)
    
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    
    # Blueprint'leri import et ve kaydet
    from .routes.auth import auth_bp
    from .routes.listings import listings_bp
    from .routes.main import main_bp
    from .routes.messages import messages_bp
    from .routes.user import user_bp
    
    app.register_blueprint(auth_bp)
    app.register_blueprint(listings_bp)
    app.register_blueprint(main_bp)
    app.register_blueprint(messages_bp)
    app.register_blueprint(user_bp)
    
    # Models'i import et
    from . import models
    
    return app