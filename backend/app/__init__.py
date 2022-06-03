__version__ = '0.1'
from flask import Flask
from flask_cors import CORS
import json


app = Flask(__name__, static_url_path='', template_folder='static')

CORS(app)
loadConfig = open('config.json')
app.config['config'] = json.load(loadConfig)

from app.routes import *

