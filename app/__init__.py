from flask import Flask, session
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager, login_manager
from datetime import timedelta
from flask_debugtoolbar import DebugToolbarExtension
from .config import APP_SECRET, DB_URI


db = SQLAlchemy()
migrate = Migrate()


def create_app():
    app = Flask(__name__, 
            static_url_path='', 
            static_folder='static',
            template_folder='templates')

    app.config['SQLALCHEMY_DATABASE_URI'] = DB_URI
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=365*2)
    app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
    app.secret_key = APP_SECRET

    toolbar = DebugToolbarExtension()

    
    db.init_app(app)
    migrate.init_app(app, db)
    toolbar.init_app(app)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login_get'
    login_manager.init_app(app)

    from .models import User
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))
    
    from .admin import admin as admin_blueprint
    app.register_blueprint(admin_blueprint)

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    from .botapi import bapi as bot_blueprint
    app.register_blueprint(bot_blueprint)
    
    app.debug = True
    return app
