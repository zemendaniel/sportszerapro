import re
from datetime import datetime
from time import sleep
from wtforms.fields.simple import StringField, BooleanField
from wtforms.fields.numeric import IntegerField, FloatField
from flask import request, render_template, abort, flash, redirect, url_for, g, make_response
from blueprints.listings import bp
from blueprints.pages import bp as base_bp
from blueprints.listings.forms import CreateListingFormMeta
from persistence.repository.listing import ListingRepository
from persistence.model.listing import Listing
from security.decorators import is_admin, is_fully_authenticated
from persistence.model.attribute import AttributeValue
from blueprints import flash_form_errors


@base_bp.route('/')
@base_bp.route('/<path:path_slug>')
def listings(path_slug=None):
    if path_slug:
        category = CategoryRepository.find_by_path_slug(path_slug) or abort(404)
        categories = category.direct_descendants
        listings_arr = ListingRepository.find_all_under_category(category)
    else:
        category = None
        categories = CategoryRepository.find_all_roots()
        listings_arr = ListingRepository.find_all()

    return render_template('listings/list.html', categories=categories, category=category, listings=listings_arr)


@bp.route('/<path:slug>')
def view(slug):
    listing = ListingRepository.find_by_slug(slug) or abort(404)

    return render_template('listings/view.html', listing=listing, category=listing.category)


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
    form = category.build_create_listing_form()

    if form.validate_on_submit():
        listing.form_update(form)
        listing.author_id = g.user.id
        listing.category = category
        listing.save()

        for field_name, field in form._fields.items():
            if field_name.startswith("attr_"):
                attr_id = int(field_name.replace("attr_", ""))
                value = field.data
                attr_value_link = AttributeValue(attribute_id=attr_id, listing_id=listing.id, value=value)
                attr_value_link.save()

        flash('Hirdetés hozzáadva.', 'success')

        return redirect(url_for('pages.listings'))
    elif form.errors:
        flash_form_errors(form)

    return render_template('listings/form.html', form=form, create=True, category=category)


@bp.route('/edit/<int:listing_id>', methods=('GET', 'POST'))
@is_fully_authenticated
def edit(listing_id):
    listing = ListingRepository.find_by_id(listing_id) or abort(404)
    if listing.author_id != g.user.id:
        abort(403)

    form = listing.category.build_create_listing_form()

    if form.validate_on_submit():
        listing.form_update(form)
        listing.save()

        for field_name, field in form._fields.items():
            if field_name.startswith("attr_"):
                attr_id = int(field_name.replace("attr_", ""))
                value = field.data
                print(value)
                try:
                    int(value)
                except ValueError:
                    value = value.strip()
                attr_value_link = AttributeValue.find(attr_id, listing_id)
                if attr_value_link:
                    attr_value_link.value = value
                else:
                    attr_value_link = AttributeValue(attribute_id=attr_id, listing_id=listing_id, value=value)
                attr_value_link.save()

        flash('Hirdetés módosítva.', 'success')
        return redirect(url_for('listings.edit', listing_id=listing.id))

    elif request.method == 'GET':
        form.process(obj=listing)
        for av in listing.attribute_value_links:
            field_name = f'attr_{av.attribute_id}'
            if field_name in form:
                form[field_name].data = av.value

    elif form.errors:
        flash_form_errors(form)

    return render_template('listings/form.html', form=form, listing=listing)


@bp.route('/delete/<int:listing_id>', methods=('POST',))
@is_fully_authenticated
def delete(listing_id):
    listing = ListingRepository.find_by_id(listing_id) or abort(404)
    if listing.author_id != g.user.id:
        abort(403)

    listing.delete()
    flash('Hirdetés törölve.', 'success')

    return redirect(url_for('listings.own'))


# @bp.route('/test/')
# def test():
#     category = CategoryRepository.find_by_id(2)
#     form = category.build_create_listing_form()
#     return render_template('listings/test.html', form=form)


@bp.route('/sajat-hirdeteseim')
@is_fully_authenticated
def own():
    listings_arr = ListingRepository.find_all_owned_by_user(g.user.id)

    return render_template('listings/own.html', listings=listings_arr)


from persistence.repository.category import CategoryRepository




