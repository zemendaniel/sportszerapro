from flask import g, session, request
from blueprints.security.routes import verify_login_token
from persistence.repository.user import UserRepository
from persistence.repository.site_setting import SiteSettingRepository


def init_app(app):
    app.before_request(__load_current_user)
    app.jinja_env.globals['is_fully_authenticated'] = lambda: g.user
    app.jinja_env.globals['is_admin'] = lambda: g.user and g.user.is_admin
    # Organization name, for example "Bolyai Technikum"
    app.jinja_env.globals['org_name'] = lambda: SiteSettingRepository.get_org_name()


def __load_current_user():
    user_id = session.get('user_id')

    if user_id is None:
        token = request.cookies.get('login_token')
        if token:
            user_id = verify_login_token(token)

    g.user = UserRepository.find_by_id(user_id) if user_id else None
