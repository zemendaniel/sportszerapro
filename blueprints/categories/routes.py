import re
from datetime import datetime
from time import sleep

from flask import request, render_template, abort, flash, redirect, url_for, g, make_response
from blueprints.categories import bp
from blueprints.categories.forms import CreateCategoryForm
from persistence.repository.category import CategoryRepository
from persistence.model.category import Category
from security.decorators import is_admin, is_fully_authenticated


@bp.route('/')
@is_fully_authenticated
@is_admin
def list_all():
    categories = CategoryRepository.find_all_roots()

    return render_template('categories/list.html', categories=categories)


@bp.route('/<int:category_id>')
@is_fully_authenticated
@is_admin
def view(category_id):
    category = CategoryRepository.find_by_id(category_id) or abort(404)

    return render_template('categories/list.html', category=category, categories=category.direct_descendants)


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

        if category.parent_id:
            return redirect(url_for('categories.view', category_id=category.parent_id))
        return redirect(url_for('categories.list_all'))

    return render_template('categories/form.html', form=form, create=True)


@bp.route('/edit/<int:category_id>', methods=('GET', 'POST'))
@is_fully_authenticated
@is_admin
def edit(category_id):
    category = CategoryRepository.find_by_id(category_id) or abort(404)
    form = CreateCategoryForm(obj=category)

    if form.validate_on_submit():
        category.form_update(form)
        category.save()
        flash("Kategória módosítva.", 'success')
        if category.parent_id:
            return redirect(url_for('categories.view', category_id=category.parent_id))
        return redirect(url_for('categories.list_all'))

    return render_template('categories/form.html', form=form, category=category)


@bp.route('/delete/<int:category_id>', methods=('POST',))
@is_fully_authenticated
@is_admin
def delete(category_id):
    category = CategoryRepository.find_by_id(category_id) or abort(404)
    category.delete()
    flash('Kategória törölve.', 'success')

    if category.parent_id:
        return redirect(url_for('categories.view', category_id=category.parent_id))
    return redirect(url_for('categories.list_all'))









