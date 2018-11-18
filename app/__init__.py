from flask import Flask
import config
from config import Config, TestConfiguration, DevelopmentConfiguration
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager


app = Flask(__name__)
app.config.from_object(config.DevelopmentConfiguration)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
login = LoginManager(app)
login.login_view = 'login'
login.login_message_category = 'info'

from app import routes, models
