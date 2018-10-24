from flask import Flask
from config_dir.config import keys

app = Flask(__name__)
app.config['SECRET_KEY'] = keys['secret_key']
