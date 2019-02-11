import os
import logging
from logging.handlers import RotatingFileHandler
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from config import Config, DevelopmentConfig
from flask_mail import Mail


app = Flask(__name__)
app.config.from_object(DevelopmentConfig)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
login = LoginManager(app)
login.login_view = 'auth.login'
login.login_message_category = 'info'

mail = Mail(app)


from app.auth import bp as auth_bp
from app.posts import bp as posts_bp
from app.main import bp as main_bp
from app.errors import bp as errors_bp

app.register_blueprint(auth_bp, url_prefix='/auth')
app.register_blueprint(posts_bp)
app.register_blueprint(main_bp)
app.register_blueprint(errors_bp)

from app import models, db

if not app.debug:
    if not os.path.exists('logs'):
        os.mkdir('logs')
    file_handler = RotatingFileHandler('logs/flask_blog', maxBytes=10240, backupCount=10)
    file_handler.setFormatter(logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
                            ))
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)

    app.logger.setLevel(logging.INFO)
    app.logger.info('Flask blog')

def creat_app(config_class=Config):
    pass
