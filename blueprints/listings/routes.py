import re
from datetime import datetime
from time import sleep

from flask import request, render_template, abort, flash, redirect, url_for, g, make_response
from blueprints.listings import bp
from blueprints.pages import bp as base_bp
from blueprints.listings.forms import CreatePostForm, EditPostForm
from persistence.repository.listing import ListingRepository
from persistence.model.listing import Listing
from security.decorators import is_admin, is_fully_authenticated


@base_bp.route('/')
def listings():
    listings_arr = ListingRepository.find_all()

    return render_template('listings/list.html', listings=listings_arr)


@bp.route('/<str:slug>')
def view(slug):
    listing = ListingRepository.find_by_slug(slug) or abort(404)

    return render_template('listings/view.html', listing=listing)


@bp.route('/uj/<int:category_id>', methods=('GET', 'POST'))
@is_fully_authenticated
def create(category_id):
    category = CategoryRepository.find_by_id(category_id) or abort(404)
    if not category.is_leaf:
        abort(403)

    listing = Listing()
    form = category.build_create_listing_form()

    if form.validate_on_submit():
        post.form_update(form)
        post.author_id = g.user.id
        post.save()
        flash('Poszt hozzáadva.', 'success')

        return redirect(url_for('listings.edit', post_id=post.id))

    return render_template('listings/form.html', form=form, create=True)


@bp.route('/edit/<int:post_id>', methods=('GET', 'POST'))
@is_fully_authenticated
@is_admin
def edit(post_id):
    post = PostRepository.find_by_id(post_id) or abort(404)
    form = EditPostForm(obj=post)

    if form.validate_on_submit():
        post.form_update(form)
        post.save()
        flash("Poszt módosítva.", 'success')
        return redirect(url_for('listings.edit', post_id=post.id))

    return render_template('listings/form.html', form=form, post=post)


@bp.route('/delete/<int:post_id>', methods=('POST',))
@is_fully_authenticated
@is_admin
def delete(post_id):
    post = PostRepository.find_by_id(post_id) or abort(404)

    PostRepository.delete(post)
    flash('Poszt törölve.', 'success')

    return redirect(url_for('pages.listings'))


@bp.route('/test/')
def test():
    category = CategoryRepository.find_by_id(2)
    form = category.build_create_listing_form()
    return render_template('listings/test.html', form=form)


from persistence.repository.category import CategoryRepository




