import os
from urllib.parse import urlsplit
from itsdangerous import URLSafeTimedSerializer, BadSignature, SignatureExpired
from flask import g, redirect, url_for, session, flash, request, render_template
from blueprints.security import bp
from blueprints.security.forms import LoginForm
from persistence.repository.user import UserRepository
from dotenv import load_dotenv
load_dotenv()

login_serializer = URLSafeTimedSerializer(os.environ['SECRET_KEY'])


def generate_login_token(user_id):
    return login_serializer.dumps(user_id, salt=os.environ['SECRET_KEY'])


def verify_login_token(token, max_age=2592000):  # 30 days in seconds
    try:
        user_id = login_serializer.loads(token, max_age=max_age, salt=os.environ['SECRET_KEY'])
    except (BadSignature, SignatureExpired):
        return None
    return user_id


@bp.route('/login', methods=('GET', 'POST'))
def login():
    if g.user is not None:
        return redirect(url_for('pages.home'))

    form = LoginForm()

    if form.validate_on_submit():
        user = UserRepository.find_by_name(form.name.data.strip())
        if user is not None and user.check_password(form.password.data):
            session['user_id'] = user.id
            flash('Sikeresen bejeltkezett!', 'success')
            if request.args.get('redirect') is not None and urlsplit(request.args.get('redirect')).netloc == '':
                response = redirect(request.args.get('redirect'))
            else:
                response = redirect(url_for('pages.home'))

            if form.stay_logged_in.data:
                token = generate_login_token(user.id)

                response.set_cookie('login_token', token, max_age=2592000, secure=True, httponly=True)

            return response

        elif user is None:
            flash('A felhasználónév hibás!', 'error')
        elif not user.check_password(form.password.data):
            flash("A jelszó hibás!", 'error')

    return render_template('security/login.html', form=form)


@bp.route('/logout', methods=['POST'])
def logout():
    session.clear()
    response = redirect(url_for('pages.home'))
    response.set_cookie('login_token', '', expires=0)
    flash('Sikeresen kijelentkezett!', 'success')
    return response











