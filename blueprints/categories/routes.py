import re
from datetime import datetime
from time import sleep

from flask import request, render_template, abort, flash, redirect, url_for, g, make_response
from blueprints.categories import bp
from blueprints.categories.forms import CreateCategoryForm
from persistence.repository.category import CategoryRepository
from persistence.repository.attribute import AttributeRepository
from persistence.model.category import Category
from security.decorators import is_admin, is_fully_authenticated
from persistence.model.attribute import CategoryAttribute


@bp.route('/')
@bp.route('/<int:category_id>')
@is_fully_authenticated
@is_admin
def list_all(category_id=None):
    if category_id:
        category = CategoryRepository.find_by_id(category_id) or abort(404)
        categories = category.direct_descendants
#        return render_template('categories/list.html', category=category, categories=category.direct_descendants)
    else:
        category = None
        categories = CategoryRepository.find_all_roots()

    query_string = (request.args.get('query_string') or '').strip().lower()
    if query_string:
        categories = [cat for cat in categories if query_string in cat.name.lower()]

    return render_template('categories/list.html', categories=categories, category=category)


# @bp.route('/<int:category_id>')
# @is_fully_authenticated
# @is_admin
# def view(category_id):
#     category = CategoryRepository.find_by_id(category_id) or abort(404)
#
#     return render_template('categories/list.html', category=category, categories=category.direct_descendants)


@bp.route('/create', methods=('GET', 'POST'))
@is_fully_authenticated
@is_admin
def create():
    category = Category()
    form = CreateCategoryForm()
    parent_id = request.args.get('parent_id')
    if form.validate_on_submit():
        category.form_update(form)
        category.parent_id = parent_id
        category.save()
        flash('Kategória hozzáadva.', 'success')

        return redirect(url_for('categories.list_all', category_id=category.parent_id))

    return render_template('categories/form.html', form=form, create=True)


@bp.route('/edit/<int:category_id>', methods=('GET', 'POST'))
@is_fully_authenticated
@is_admin
def edit(category_id):
    category = CategoryRepository.find_by_id(category_id) or abort(404)
    form = CreateCategoryForm(obj=category)
    attributes = AttributeRepository.find_all_not_default()

    if form.validate_on_submit():
        category.form_update(form)
        category.save()
        flash("Kategória módosítva.", 'success')
        return redirect(url_for('categories.edit', category_id=category_id))

    return render_template('categories/form.html', form=form, category=category, attributes=attributes)


@bp.route('/delete/<int:category_id>', methods=('POST',))
@is_fully_authenticated
@is_admin
def delete(category_id):
    category = CategoryRepository.find_by_id(category_id) or abort(404)
    category.delete()
    flash('Kategória törölve.', 'success')

    return redirect(url_for('categories.list_all', category_id=category.parent_id))


@bp.route('/set_attributes/<int:category_id>', methods=('POST',))
@is_fully_authenticated
@is_admin
def set_attributes(category_id):
    category = CategoryRepository.find_by_id(category_id) or abort(404)
    # if not category.is_leaf:
    #     abort(403)

    attribute = AttributeRepository.find_by_id(int(request.form['attribute_id'])) or abort(404)
    bool_value = request.form.get('bool_value') == 'on'

    if category.attribute_is_inherited_or_default(attribute):
        abort(403)

    if bool_value:
        CategoryAttribute.create(category, attribute)
    else:
        CategoryAttribute.remove(category, attribute)

    flash('Kategória módosítva.', 'success')

    return redirect(url_for('categories.edit', category_id=category_id))









