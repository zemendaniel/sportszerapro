import re
from datetime import datetime
from time import sleep

from flask import request, render_template, abort, flash, redirect, url_for, g, make_response
from blueprints.listings import bp
from blueprints.pages import bp as base_bp
from blueprints.listings.forms import CreateListingFormMeta
from persistence.repository.listing import ListingRepository
from persistence.model.listing import Listing
from security.decorators import is_admin, is_fully_authenticated
from persistence.model.attribute import AttributeValue


@base_bp.route('/')
@base_bp.route('/<path:path_slug>')
def listings(path_slug=None):
    if path_slug:
        category = CategoryRepository.find_by_path_slug(path_slug) or abort(404)
        categories = category.direct_descendants
    else:
        category = None
        categories = CategoryRepository.find_all_roots()

    # listings_arr = ListingRepository.find_all()

    return render_template('listings/list.html', categories=categories, category=category)


@bp.route('/<string:slug>')
def view(slug):
    listing = ListingRepository.find_by_slug(slug) or abort(404)

    return render_template('listings/view.html', listing=listing)


@is_fully_authenticated
@bp.route('/kategoria-valaszto')
@bp.route('/kategoria-valaszto/<int:category_id>')
def category_selector(category_id=None):
    if category_id:
        category = CategoryRepository.find_by_id(category_id) or abort(404)
        categories = category.direct_descendants
    else:
        category = None
        categories = CategoryRepository.find_all_roots()

    return render_template('listings/category_selector.html', category=category, categories=categories)


@bp.route('/uj/<int:category_id>', methods=('GET', 'POST'))
@is_fully_authenticated
def create(category_id):
    category = CategoryRepository.find_by_id(category_id) or abort(404)
    if not category.is_leaf:
        abort(403)

    listing = Listing()
    form_meta = CreateListingFormMeta()
    form = category.build_create_listing_form()

    if form_meta.validate_on_submit() and form.validate_on_submit():
        listing.form_update(form)
        listing.author_id = g.user.id
        listing.save()

        for field_name, field in form._fields.items():
            if field_name.startswith("attr_"):
                attr_id = int(field_name.replace("attr_", ""))
                value = field.data
                attr_value_link = AttributeValue(attribute_id=attr_id, listing_id=listing.id, value=value)
                attr_value_link.save()

        flash('Hirdetés hozzáadva.', 'success')

        return redirect(url_for('pages.listings'))

    return render_template('listings/form.html', form=form, create=True, category=category, form_meta=form_meta)


# @bp.route('/edit/<int:post_id>', methods=('GET', 'POST'))
# @is_fully_authenticated
# @is_admin
# def edit(post_id):
#     post = PostRepository.find_by_id(post_id) or abort(404)
#     form = EditPostForm(obj=post)
#
#     if form.validate_on_submit():
#         post.form_update(form)
#         post.save()
#         flash("Poszt módosítva.", 'success')
#         return redirect(url_for('listings.edit', post_id=post.id))
#
#     return render_template('listings/form.html', form=form, post=post)
#
#
# @bp.route('/delete/<int:post_id>', methods=('POST',))
# @is_fully_authenticated
# @is_admin
# def delete(post_id):
#     post = PostRepository.find_by_id(post_id) or abort(404)
#
#     PostRepository.delete(post)
#     flash('Poszt törölve.', 'success')
#
#     return redirect(url_for('pages.listings'))


@bp.route('/test/')
def test():
    category = CategoryRepository.find_by_id(2)
    form = category.build_create_listing_form()
    return render_template('listings/test.html', form=form)


from persistence.repository.category import CategoryRepository




