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

    #mail configuration for sending logs
    MAIL_SERVER = MailSettings.MAIL_SERVER
    MAIL_PORT = MailSettings.MAIL_PORT
    MAIL_USE_TLS = MailSettings.MAIL_USE_TLS
    MAIL_USERNAME = MailSettings.MAIL_USERNAME
    MAIL_PASSWORD = MailSettings.MAIL_PASSWORD
    ADMINS = MailSettings.ADMINS


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
