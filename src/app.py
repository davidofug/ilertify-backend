"""Flask Application"""

# load libraries
from flask import Flask
from flask_cors import CORS
import sys

from flask.helpers import url_for

# load modules
from src.blueprints.products import products
from src.blueprints.members import members

# init Flask app

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

# register blueprints. ensure that all paths are versioned!
app.register_blueprint(products, url_prefix="/api/v1/products")
app.register_blueprint(members, url_prefix="/api/v1/members")