from flask import Blueprint

bp = Blueprint('attributes', __name__)

from blueprints.attributes import routes
