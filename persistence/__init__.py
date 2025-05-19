import click
from alchemical.flask import Alchemical
from flask import g
from dotenv import load_dotenv
load_dotenv()

db = Alchemical()


def init_app(app):
    app.cli.add_command(__install_command)
    app.cli.add_command(___command)
    app.before_request(__on_before_request)
    app.teardown_appcontext(__on_teardown_appcontext)

    db.init_app(app)


def install():
    db.drop_all()
    db.create_all()

    reset_admin()


def reset_admin():
    with db.Session() as session:
        admin = session.scalar(User.select().where(User.role == 'super_admin'))
        if admin:
            session.delete(admin)
            session.commit()
        admin = User()

        while True:
            name = input("Admin neve (max. 64 karakter hosszú): ").strip()
            if len(name) <= 64:
                break

        while True:
            password = input("Admin jelszava (min. 4, max. 32 karakter hosszú): ")
            if 4 <= len(password) <= 32:
                break

        # DON'T USE THE USUAL METHODS AS THEY REQUIRE A G.SESSION
        admin.name = name
        admin.password = password
        # THIS HAS TO BE WITH THE _ROLE NOT ROLE
        admin._role = 'super_admin'

        session.add(admin)
        session.commit()


@click.command('install')
def __install_command():
    install()
    click.echo('Application installation successful.')


@click.command('reset-admin')
def ___command():
    reset_admin()
    click.echo('Admin reset successful.')


def __on_before_request():
    if 'session' not in g:
        g.session = db.Session()


def __on_teardown_appcontext(e):
    if 'session' in g:
        g.pop('session').close()


from persistence.model.user import User
