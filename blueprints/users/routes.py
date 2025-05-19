from flask import g, redirect, url_for, flash, render_template, abort, request, session
from security.decorators import is_admin, is_fully_authenticated
from blueprints.users import bp
from blueprints.pages import bp as base_bp
from blueprints.users.forms import RegisterUserForm, EditUserRoleForm, UserSettingsForm, UserPasswordResetForm, \
    UserDeleteForm
from persistence.repository.user import UserRepository
from persistence.model.user import User


@bp.route('/', methods=['GET', 'POST'])
@is_fully_authenticated
@is_admin
def list_all():
    users = UserRepository.find_all()
    role_form = EditUserRoleForm()

    if role_form.validate_on_submit():
        user = UserRepository.find_by_id(role_form.user_id.data) or abort(404)
        if user.is_super_admin or g.user.id == user.id:
            abort(403)

        user.role = role_form.role.data
        user.save()
        flash(f"{user.name} szerepköre sikeresen megváltozva erre: {user.role_hun}", 'success')
        return redirect(url_for('users.list_all'))

    return render_template("users/list.html", users=users, role_form=role_form)


@bp.route('/delete/<int:user_id>', methods=['POST'])
@is_fully_authenticated
@is_admin
def delete(user_id):
    user = UserRepository.find_by_id(user_id) or abort(404)
    if user.is_super_admin or g.user.id == user.id:
        abort(403)

    username = user.name
    user.delete()
    flash(f"{username} fiókja sikeresen törölve.", 'success')
    return redirect(url_for('users.list_all'))


@base_bp.route('/register', methods=['GET', 'POST'])
def register():
    if g.user is not None:
        return redirect(url_for('pages.home'))

    form = RegisterUserForm()
    user = User()
    if form.validate_on_submit():
        if UserRepository.find_by_name(form.name.data.strip()):
            flash('A név már foglalt!', 'error')
            return redirect(url_for('pages.register'))
        user.form_update(form)
        user.save()
        flash("Sikeres regisztráció!", 'success')

        return redirect(url_for('security.login'))

    return render_template('users/register.html', form=form)


@base_bp.route('/settings')
@is_fully_authenticated
def settings():

    user_settings_form = UserSettingsForm()
    user_password_form = UserPasswordResetForm()
    user_delete_form = UserDeleteForm()

    user_settings_form.name.data = g.user.name

    return render_template('users/settings.html', user_settings_form=user_settings_form, user_password_form=user_password_form, user_delete_form=user_delete_form)


@bp.route('/user_settings', methods=['POST'])
@is_fully_authenticated
def user_settings():
    user = g.user
    user_settings_form = UserSettingsForm()

    if user_settings_form.validate_on_submit():
        if UserRepository.find_by_name(user_settings_form.name.data.strip()):
            flash('A név már foglalt!', 'error')
            return redirect(url_for('pages.settings'))

        user.name = user_settings_form.name.data
        user.save()

        flash("A felhasználónév sikeresen megváltozott!", 'success')

    return redirect(url_for('pages.settings'))


@bp.route('/password_reset', methods=['POST'])
@is_fully_authenticated
def password_reset():
    user = g.user
    user_password_form = UserPasswordResetForm()

    if user_password_form.validate_on_submit():
        if user.check_password(user_password_form.old_password.data):
            user.password = user_password_form.new_password.data
            user.save()
            flash("A jelszó sikeresen megváltozott!", 'success')
        else:
            flash("A régi jelszó hibás!", 'error')

    return redirect(url_for('pages.settings'))


@is_fully_authenticated
@bp.route('/delete-self', methods=['POST'])
def delete_self():
    user = g.user
    user_delete_form = UserDeleteForm()

    if user.is_super_admin:
        abort(403)

    if user_delete_form.validate_on_submit():
        if not user.check_password(user_delete_form.password.data):
            flash("A jelszó hibás, sikertelen törlés!", 'error')
            return redirect(url_for('pages.settings'))
        user.delete()
        flash("Fiók sikeresen törölve.", 'success')

    return redirect(url_for('security.login'))

