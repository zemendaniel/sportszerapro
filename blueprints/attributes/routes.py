import re
from datetime import datetime
from time import sleep

from flask import request, render_template, abort, flash, redirect, url_for, g, make_response
from blueprints.attributes import bp
from blueprints.attributes.forms import CreateAttributeForm
from persistence.repository.attribute import AttributeRepository
from persistence.model.attribute import Attribute
from security.decorators import is_admin, is_fully_authenticated


@bp.route('/')
@is_fully_authenticated
@is_admin
def list_all():
    query_string = (request.args.get('query_string') or '').strip().lower()
    if query_string:
        attributes = AttributeRepository.find_by_name_like(query_string)
    else:
        attributes = AttributeRepository.find_all()

    return render_template('attributes/list.html', attributes=attributes)


@bp.route('/create', methods=('GET', 'POST'))
@is_fully_authenticated
@is_admin
def create():
    attribute = Attribute()
    form = CreateAttributeForm()
    if form.validate_on_submit():
        attribute.form_update(form)
        attribute.save()
        flash('Tulajdonság hozzáadva.', 'success')

        return redirect(url_for('attributes.list_all'))

    return render_template('attributes/form.html', form=form, create=True)


@bp.route('/edit/<int:attribute_id>', methods=('GET', 'POST'))
@is_fully_authenticated
@is_admin
def edit(attribute_id):
    attribute = AttributeRepository.find_by_id(attribute_id) or abort(404)
    form = CreateAttributeForm(obj=attribute)

    if form.validate_on_submit():
        attribute.form_update(form)
        attribute.save()
        flash("Tulajdonság módosítva.", 'success')
        return redirect(url_for('attributes.edit', attribute_id=attribute.id))
    return render_template('attributes/form.html', form=form, attribute=attribute)


@bp.route('/delete/<int:attribute_id>', methods=('POST',))
@is_fully_authenticated
@is_admin
def delete(attribute_id):
    attribute = AttributeRepository.find_by_id(attribute_id) or abort(404)
    attribute.delete()
    flash('Tulajdonság törölve.', 'success')

    return redirect(url_for('attributes.list_all'))









