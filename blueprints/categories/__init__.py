from flask import Blueprint

bp = Blueprint('categories', __name__)

from blueprints.categories import routes
