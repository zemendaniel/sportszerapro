import os
import logging
import persistence
from logging.handlers import RotatingFileHandler
from flask import Flask, render_template
import blueprints.listings
import blueprints.security
import blueprints.pages
import blueprints.users
import blueprints.categories
import blueprints.attributes
import security
from flask_wtf.csrf import CSRFProtect
from config import Config
from flask_minify import Minify
from jinja2 import Environment, PackageLoader, select_autoescape, FileSystemLoader
from blueprints.pages import init_error_handlers
from custom_filters import safe_escape
from flask_ckeditor import CKEditor

csrf = CSRFProtect()
minify = Minify(html=True, js=True, cssless=True)
ckeditor = CKEditor()


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    app.jinja_env.filters['safe_escape'] = safe_escape
    app.jinja_env.add_extension('jinja2.ext.do')

    app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
        'pool_size': 10,
        'max_overflow': 20,
        'pool_timeout': 30,
        'pool_recycle': 1800,
    }
    persistence.init_app(app)
    security.init_app(app)
    csrf.init_app(app)
    minify.init_app(app)
    init_error_handlers(app)
    ckeditor.init_app(app)

    app.register_blueprint(blueprints.listings.bp, url_prefix='/')
    app.register_blueprint(blueprints.pages.bp, url_prefix='/')
    app.register_blueprint(blueprints.security.bp, url_prefix='/')
    app.register_blueprint(blueprints.users.bp, url_prefix='/users')
    app.register_blueprint(blueprints.categories.bp, url_prefix='/categories')
    app.register_blueprint(blueprints.attributes.bp, url_prefix='/attributes')

    handler = RotatingFileHandler('errors.log')
    handler.setLevel(logging.ERROR)
    app.logger.addHandler(handler)

    return app


if __name__ == '__main__':
    create_app().run(host="0.0.0.0", debug=True)

