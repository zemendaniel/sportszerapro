from flask import Blueprint, render_template
from flask_wtf.csrf import CSRFError

bp = Blueprint('pages', __name__)

from blueprints.pages import routes
# from blueprints.users.routes import settings


def init_error_handlers(app):
    @app.errorhandler(500)
    def internal_server_error(error):
        app.logger.error('Server Error: %s', error)
        return render_template('errors/500.html'), 500

    @app.errorhandler(404)
    def not_found(error):
        return render_template('errors/404.html'), 404

    @app.errorhandler(401)
    def unauthorized(error):
        return render_template('errors/401.html'), 401

    @app.errorhandler(403)
    def forbidden(error):
        return render_template('errors/403.html'), 403

    @app.errorhandler(405)
    def method_not_allowed(error):
        return render_template('errors/405.html'), 405

    @app.errorhandler(CSRFError)
    def handle_csrf_error(e):
        return render_template('errors/400.html'), 400
