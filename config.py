import os
from dotenv import load_dotenv
from mail_config import MailSettings

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))


class Config(object):
    ENV = 'development'
    TESTING = False
    DEBUG = False
    CSRF_ENABLED = True
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'hard_to_guess_12345678'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URI') or 'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    LANGUAGES = ['en', 'pl']

    #mail configuration for sending logs and emails to reset password
    MAIL_SERVER = MailSettings.server
    MAIL_PORT = MailSettings.port
    MAIL_USE_TLS = MailSettings.use_tls
    MAIL_USERNAME = MailSettings.username
    MAIL_PASSWORD = MailSettings.password
    ADMINS = ['testblazej2018@gmail.com']


class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True


class ProductionConfig(Config):
    ENV = 'production'
    DEBUG = False


class StagingConfig(Config):
    DEVELOPMENT = True
    DEBUG = True
