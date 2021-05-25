"""Flask Application"""

# load libraries
from flask import Flask, jsonify
import sys

from flask.helpers import url_for

# load modules
from src.endpoints.products import products
from src.endpoints.members import members

# init Flask app

app = Flask(__name__)

# register blueprints. ensure that all paths are versioned!
app.register_blueprint(products, url_prefix="/api/v1/products")
app.register_blueprint(members, url_prefix="/api/v1/members")
