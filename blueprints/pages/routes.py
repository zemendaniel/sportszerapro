from flask import redirect, url_for, render_template, request, g, flash, abort, send_file
from blueprints.pages import bp
from security.decorators import is_fully_authenticated, is_admin
from blueprints.pages.forms import SetOrgNameForm, SetFaviconForm, SetWelcomeTextForm
from persistence.repository.site_setting import SiteSettingRepository
from io import BytesIO


@bp.route('/')
def home():
    return render_template('pages/home.html', welcome_text=SiteSettingRepository.get_welcome_text())


@bp.route('/site-settings', methods=['GET', 'POST'])
@is_fully_authenticated
@is_admin
def site_settings():
    org_form = SetOrgNameForm()
    icon_form = SetFaviconForm()
    welcome_form = SetWelcomeTextForm()

    if org_form.validate_on_submit():
        SiteSettingRepository.set_org_name(org_form.name.data.strip())
        flash("A szervezet neve sikeresen beállítva!", 'success')
        return redirect(url_for('pages.site_settings'))
    else:
        org_form.name.data = SiteSettingRepository.get_org_name()

    if welcome_form.is_submitted():
        if welcome_form.validate():
            SiteSettingRepository.set_welcome_text(welcome_form.text.data)
            flash("Üdvözlő szöveg sikeresen beállítva!", 'success')
            return redirect(url_for('pages.site_settings'))
        elif welcome_form.errors:
            for field, err in welcome_form.errors.items():
                for error in err:
                    flash(error, 'error')
            return redirect(url_for('pages.site_settings'))
    else:
        welcome_form.text.data = SiteSettingRepository.get_welcome_text()

    # This has to be the last form validation
    if icon_form.is_submitted():
        if icon_form.validate():
            SiteSettingRepository.set_favicon(icon_form.icon.data)
            flash("A favicon sikeresen beállítva!"
                  "|Lehetséges, hogy üríteni kell a gyorsítótárat, hogy az új ikon jelenjen meg.", 'success')
            return redirect(url_for('pages.site_settings'))
        elif icon_form.errors:
            for field, err in icon_form.errors.items():
                for error in err:
                    flash(error, 'error')
            return redirect(url_for('pages.site_settings'))

    return render_template('pages/site-settings.html', org_form=org_form, icon_form=icon_form,
                           favicon_exits=bool(SiteSettingRepository.find_by_key('favicon')), welcome_form=welcome_form)


@bp.route('/delete-favicon', methods=['POST'])
@is_fully_authenticated
@is_admin
def delete_favicon():
    icon = SiteSettingRepository.find_by_key('favicon') or abort(404)
    SiteSettingRepository.delete(icon)
    flash("A favicon sikeresen törölve!|Lehetséges, hogy üríteni kell a gyorsítótárat,"
          " hogy a változtatások látszódjanak.", 'success')
    return redirect(url_for('pages.site_settings'))


@bp.route('/favicon.ico')
def favicon():
    icon = SiteSettingRepository.get_favicon() or abort(404)

    return send_file(BytesIO(icon), mimetype='application/octet-stream', as_attachment=False, download_name='favicon.ico')


@bp.route('/errors')
@is_fully_authenticated
@is_admin
def errors():
    if request.args.get('delete'):
        with open('errors.log', 'w') as f:
            f.write('')
        return redirect(url_for('pages.errors'))

    try:
        with open('errors.log', 'r') as f:
            errors_text = f.read().replace('\n', '<br>')
    except FileNotFoundError:
        errors_text = ""

    return render_template("errors/errors.html", errors=errors_text)


@bp.route("/about")
def about():
    return render_template("pages/about.html")
