from flask import Blueprint

bp = Blueprint('posts', __name__)

from blueprints.posts import routes
