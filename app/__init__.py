import os
import logging
from logging.handlers import RotatingFileHandler


from flask import Flask, request, current_app
from flask_babel import Babel, lazy_gettext as _l
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_moment import Moment
from flask_mail import Mail
from flask_sqlalchemy import SQLAlchemy
from config import Config, DevelopmentConfig
from flask_bootstrap import Bootstrap
import flask_whooshalchemy as wa


db = SQLAlchemy()
migrate = Migrate()
login = LoginManager()
login.login_view = 'auth.login'
login.login_message = _l('Please log in to access this page')
mail = Mail()
moment = Moment()
babel = Babel()
bootstrap = Bootstrap()


def create_app(config_class=DevelopmentConfig):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    migrate.init_app(app, db)
    login.init_app(app)
    mail.init_app(app)
    moment.init_app(app)
    babel.init_app(app)
    bootstrap.init_app(app)
    wa.search_index(app, models.Post)

    from app.auth import bp as auth_bp
    from app.posts import bp as posts_bp
    from app.main import bp as main_bp
    from app.errors import bp as errors_bp
    from app.admin import bp as admin_bp

    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(admin_bp, url_prefix='/admin')
    app.register_blueprint(posts_bp)
    app.register_blueprint(main_bp)
    app.register_blueprint(errors_bp)



    if not app.debug and not app.testing:
        if not os.path.exists('logs'):
            os.mkdir('logs')
        file_handler = RotatingFileHandler('logs/flask_blog',
                                           maxBytes=10240,
                                           backupCount=10)
        file_handler.setFormatter(logging.Formatter(
            '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
        ))
        file_handler.setLevel(logging.INFO)
        app.logger.addHandler(file_handler)

        app.logger.setLevel(logging.INFO)
        app.logger.info('Flask blog')

    return app


@babel.localeselector
def get_locale():
    return request.accept_languages.best_match(current_app.config['LANGUAGES'])


from app import models
