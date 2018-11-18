import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    TESTING = False
    DEBUG = False
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'hard_to_guess_12345678'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class DevelopmentConfiguration(Config):
    DEBUG = True


class TestConfiguration(Config):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'test.db')
    WTF_CSRF_ENABLED = False
    TESTING = True
