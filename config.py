import os

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'hard_to_guess_12345678'