from flask import Blueprint

bp = Blueprint('listings', __name__)

from blueprints.listings import routes
