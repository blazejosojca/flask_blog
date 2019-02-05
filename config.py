import os
from mail_config import MailSettings
basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    ENV = 'development'
    TESTING = False
    DEBUG = False
    CSRF_ENABLED = True
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'hard_to_guess_12345678'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

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


class TestConfig(Config):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'test.db')
    TESTING = True
