""" import modules """
import os
from dotenv import load_dotenv
from mail_config import MailSettings

BASEDIR = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(BASEDIR, '.env'))


class Config(object):
    """
    Base configuration class. With default values
    """
    ENV = 'development'
    TESTING = False
    DEBUG = False
    CSRF_ENABLED = True
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'hard_to_guess_12345678'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URI') \
                    or 'sqlite:///' + os.path.join(BASEDIR, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    LANGUAGES = ['en', 'pl']

    MAIL_SERVER = MailSettings.server
    MAIL_PORT = MailSettings.port
    MAIL_USE_TLS = MailSettings.use_tls
    MAIL_USERNAME = MailSettings.username
    MAIL_PASSWORD = MailSettings.password
    ADMINS = ['testblazej2018@gmail.com']
    MS_TRANSLATOR_KEY = os.environ.get('MS_TRANSLATOR_KEY')



class DevelopmentConfig(Config):
    """ Configuration for development enviroment """
    DEVELOPMENT = True
    DEBUG = True



class ProductionConfig(Config):
    """ Configuration for production enviroment. Without debug mode. """
    ENV = 'production'
    DEBUG = False


class StagingConfig(Config):
    """ Configuration for staging enviroment """
    DEVELOPMENT = True
    DEBUG = True
