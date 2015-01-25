# -*- coding: utf-8 -*-

from cStringIO import StringIO
from csv import QUOTE_ALL, writer

from flask import (
    abort,
    Blueprint,
    flash,
    g,
    redirect,
    render_template,
    request,
    Response,
    session,
    url_for,
)

from modules import classes
from modules import decorators
from modules import forms
from modules import models
from modules import utilities

blueprint = Blueprint('administrators', __name__)


@blueprint.before_request
def before_request():
    g.administrator = None
    if 'administrator' in session:
        g.administrator = True


@blueprint.route('/')
@decorators.requires_administrator
def dashboard():
    return render_template(
        'administrators/views/dashboard.html',
        categories=utilities.get_integer(
            g.mysql.query(models.category).count()
        ),
        handles=utilities.get_integer(g.mysql.query(models.handle).count()),
        tweets=utilities.get_integer(g.mysql.query(models.tweet).count()),
    )


@blueprint.route('/categories/overview')
@decorators.requires_administrator
def categories_overview():
    return render_template(
        'administrators/views/categories_overview.html',
        categories=g.mysql.query(
            models.category,
        ).order_by('position asc').all(),
    )


@blueprint.route('/categories/add', methods=['GET', 'POST'])
@decorators.requires_administrator
def categories_add():
    category = models.category()
    form = forms.categories_form(request.form, category)
    form.id = category.id
    if request.method == 'POST':
        if form.validate_on_submit():
            category.position = category.get_position()
            g.mysql.add(form.get_instance(category))
            g.mysql.commit()
            flash('The category was saved successfully.', 'success')
            return redirect(url_for('administrators.categories_overview'))
        flash('The category was not saved successfully.', 'danger')
    return render_template(
        'administrators/views/categories_add.html', form=form,
    )


@blueprint.route('/categories/<int:id>/edit', methods=['GET', 'POST'])
@decorators.requires_administrator
def categories_edit(id):
    category = g.mysql.query(models.category).get(id)
    if not category:
        abort(404)
    form = forms.categories_form(request.form, category)
    form.id = category.id
    if request.method == 'POST':
        if form.validate_on_submit():
            g.mysql.add(form.get_instance(category))
            g.mysql.commit()
            flash('The category was updated successfully.', 'success')
            return redirect(url_for('administrators.categories_overview'))
        flash('The category was not updated successfully.', 'danger')
    return render_template(
        'administrators/views/categories_edit.html', form=form, id=id,
    )


@blueprint.route('/categories/<int:id>/position/<direction>')
@decorators.requires_administrator
def categories_position(id, direction):
    category = g.mysql.query(models.category).get(id)
    if not category:
        abort(404)
    category.set_position(direction)
    return redirect(url_for('administrators.categories_overview'))


@blueprint.route('/categories/<int:id>/delete', methods=['GET', 'POST'])
@decorators.requires_administrator
def categories_delete(id):
    category = g.mysql.query(models.category).get(id)
    if not category:
        abort(404)
    if request.method == 'GET':
        return render_template(
            'administrators/views/categories_delete.html', id=id
        )
    if request.method == 'POST':
        g.mysql.delete(category)
        g.mysql.commit()
        flash('The category was deleted successfully.', 'success')
        return redirect(url_for('administrators.categories_overview'))


@blueprint.route('/categories/process', methods=['GET', 'POST'])
@decorators.requires_administrator
def categories_process():
    if request.method == 'POST':
        if request.form['submit'] == 'delete':
            ids = request.form.getlist('ids')
            if ids:
                for id in ids:
                    g.mysql.delete(g.mysql.query(models.category).get(id))
                    g.mysql.commit()
                flash(
                    'The selected categories were deleted successfully.',
                    'success'
                )
            else:
                flash(
                    'Please select atleast one category and try again.',
                    'failure'
                )
    return redirect(url_for('administrators.categories_overview'))


@blueprint.route('/neighborhoods/overview')
@decorators.requires_administrator
def neighborhoods_overview():
    return render_template(
        'administrators/views/neighborhoods_overview.html',
        neighborhoods=g.mysql.query(
            models.neighborhood,
        ).order_by('position asc').all(),
    )


@blueprint.route('/neighborhoods/process', methods=['GET', 'POST'])
@decorators.requires_administrator
def neighborhoods_process():
    if request.method == 'POST':
        if request.form['submit'] == 'delete':
            ids = request.form.getlist('ids')
            if ids:
                for id in ids:
                    g.mysql.delete(g.mysql.query(models.neighborhood).get(id))
                    g.mysql.commit()
                flash(
                    'The selected neighborhoods were deleted successfully.',
                    'success'
                )
            else:
                flash(
                    'Please select atleast one neighborhood and try again.',
                    'failure'
                )
    return redirect(url_for('administrators.neighborhoods_overview'))


@blueprint.route('/neighborhoods/<int:id>/position/<direction>')
@decorators.requires_administrator
def neighborhoods_position(id, direction):
    neighborhood = g.mysql.query(models.neighborhood).get(id)
    if not neighborhood:
        abort(404)
    neighborhood.set_position(direction)
    return redirect(url_for('administrators.neighborhoods_overview'))


@blueprint.route('/neighborhoods/add', methods=['GET', 'POST'])
@decorators.requires_administrator
def neighborhoods_add():
    neighborhood = models.neighborhood()
    form = forms.neighborhoods_form(request.form, neighborhood)
    form.id = neighborhood.id
    if request.method == 'POST':
        if form.validate_on_submit():
            neighborhood.position = neighborhood.get_position()
            g.mysql.add(form.get_instance(neighborhood))
            g.mysql.commit()
            flash('The neighborhood was saved successfully.', 'success')
            return redirect(url_for('administrators.neighborhoods_overview'))
        flash('The neighborhood was not saved successfully.', 'danger')
    return render_template(
        'administrators/views/neighborhoods_add.html', form=form,
    )


@blueprint.route('/neighborhoods/<int:id>/edit', methods=['GET', 'POST'])
@decorators.requires_administrator
def neighborhoods_edit(id):
    neighborhood = g.mysql.query(models.neighborhood).get(id)
    if not neighborhood:
        abort(404)
    form = forms.neighborhoods_form(request.form, neighborhood)
    form.id = neighborhood.id
    if request.method == 'POST':
        if form.validate_on_submit():
            g.mysql.add(form.get_instance(neighborhood))
            g.mysql.commit()
            flash('The neighborhood was updated successfully.', 'success')
            return redirect(url_for('administrators.neighborhoods_overview'))
        flash('The neighborhood was not updated successfully.', 'danger')
    return render_template(
        'administrators/views/neighborhoods_edit.html', form=form, id=id,
    )


@blueprint.route('/neighborhoods/<int:id>/delete', methods=['GET', 'POST'])
@decorators.requires_administrator
def neighborhoods_delete(id):
    neighborhood = g.mysql.query(models.neighborhood).get(id)
    if not neighborhood:
        abort(404)
    if request.method == 'GET':
        return render_template(
            'administrators/views/neighborhoods_delete.html', id=id
        )
    if request.method == 'POST':
        g.mysql.delete(neighborhood)
        g.mysql.commit()
        flash('The neighborhood was deleted successfully.', 'success')
        return redirect(url_for('administrators.neighborhoods_overview'))


@blueprint.route('/handles/overview')
@decorators.requires_administrator
def handles_overview():
    filters, order_by, limit, page = utilities.get_filters_order_by_limit_page(
        'handles',
        {},
        {
            'column': 'handles.id',
            'direction': 'asc',
        },
        10,
        1
    )
    form = forms.handles_filters(**filters)
    query = form.apply(g.mysql.query(models.handle))
    pager = classes.pager(query.count(), limit, page)
    return render_template(
        'administrators/views/handles_overview.html',
        form=form,
        handles=query.order_by('%(column)s %(direction)s' % order_by).all()[
            pager.prefix:pager.suffix
        ],
        order_by=order_by,
        pager=pager,
    )


@blueprint.route('/handles/add', methods=['GET', 'POST'])
@decorators.requires_administrator
def handles_add():
    handle = models.handle()
    form = forms.handles_form(request.form, handle)
    form.id = handle.id
    if request.method == 'POST':
        if form.validate_on_submit():
            g.mysql.add(form.get_instance(handle))
            g.mysql.commit()
            flash('The handle was saved successfully.', 'success')
            return redirect(url_for('administrators.handles_overview'))
        flash('The handle was not saved successfully.', 'danger')
    return render_template(
        'administrators/views/handles_add.html', form=form,
    )


@blueprint.route('/handles/<int:id>/edit', methods=['GET', 'POST'])
@decorators.requires_administrator
def handles_edit(id):
    handle = g.mysql.query(models.handle).get(id)
    if not handle:
        abort(404)
    form = forms.handles_form(request.form, handle)
    form.id = handle.id
    if request.method == 'POST':
        if form.validate_on_submit():
            g.mysql.add(form.get_instance(handle))
            g.mysql.commit()
            flash('The handle was updated successfully.', 'success')
            return redirect(url_for('administrators.handles_overview'))
        flash('The handle was not updated successfully.', 'danger')
    return render_template(
        'administrators/views/handles_edit.html', form=form, id=id,
    )


@blueprint.route('/handles/<int:id>/delete', methods=['GET', 'POST'])
@decorators.requires_administrator
def handles_delete(id):
    handle = g.mysql.query(models.handle).get(id)
    if not handle:
        abort(404)
    if request.method == 'GET':
        return render_template(
            'administrators/views/handles_delete.html', id=id,
        )
    if request.method == 'POST':
        g.mysql.delete(handle)
        g.mysql.commit()
        flash('The handle was deleted successfully.', 'success')
        return redirect(url_for('administrators.handles_overview'))


@blueprint.route('/handles/process', methods=['GET', 'POST'])
@decorators.requires_administrator
def handles_process():
    if request.method == 'GET':
        utilities.set_order_by_limit_page('handles')
    if request.method == 'POST':
        utilities.set_filters('handles', forms.handles_filters)
        if request.form['submit'] == 'delete':
            ids = request.form.getlist('ids')
            if ids:
                for id in ids:
                    g.mysql.delete(g.mysql.query(models.handle).get(id))
                    g.mysql.commit()
                flash(
                    'The selected handles were deleted successfully.',
                    'success'
                )
            else:
                flash(
                    'Please select atleast one handle and try again.',
                    'failure'
                )
    return redirect(url_for('administrators.handles_overview'))


@blueprint.route('/visitors/overview', methods=['GET', 'POST'])
@decorators.requires_administrator
def visitors_overview():
    filters, order_by, limit, page = utilities.get_filters_order_by_limit_page(
        'visitors',
        {},
        {
            'column': 'timestamp',
            'direction': 'desc',
        },
        10,
        1
    )
    form = forms.visitors_filters(**filters)
    query = form.apply(g.mysql.query(models.visitor))
    pager = classes.pager(query.count(), limit, page)
    return render_template(
        'administrators/views/visitors_overview.html',
        form=form,
        order_by=order_by,
        pager=pager,
        visitors=query.order_by('%(column)s %(direction)s' % order_by).all()[
            pager.prefix:pager.suffix
        ],
    )


@blueprint.route('/visitors/process', methods=['GET', 'POST'])
@decorators.requires_administrator
def visitors_process():
    if request.method == 'GET':
        utilities.set_order_by_limit_page('visitors')
    if request.method == 'POST':
        utilities.set_filters('visitors', forms.visitors_filters)
    return redirect(url_for('administrators.visitors_overview'))


@blueprint.route('/visitors/export')
@decorators.requires_administrator
def visitors_export():
    filters, _, _, _ = utilities.get_filters_order_by_limit_page(
        'visitors',
        {},
        {
            'column': 'timestamp',
            'direction': 'desc',
        },
        10,
        1
    )
    csv = StringIO()
    writer(
        csv,
        delimiter=',',
        doublequote=True,
        lineterminator='\n',
        quotechar='"',
        quoting=QUOTE_ALL,
        skipinitialspace=True
    ).writerows([[
        'ID',
        'Email',
        'Timestamp',
    ]] + [
        [
            visitor.id,
            visitor.email,
            visitor.timestamp.isoformat(' '),
        ]
        for visitor in forms.visitors_filters(
            **filters
        ).apply(
            g.mysql.query(models.visitor)
        ).order_by('timestamp desc').all()
    ])
    return Response(
        csv.getvalue(),
        headers={
            'Content-Disposition': 'attachment; filename=export.csv',
        },
        mimetype='text/csv',
    )


@blueprint.route('/profile', methods=['GET', 'POST'])
@decorators.requires_administrator
def profile():
    form = forms.profile(request.form, username=g.mysql.query(
        models.setting,
    ).filter(
        models.setting.key == 'username',
    ).first().value)
    if request.method == 'POST':
        if form.validate_on_submit():
            form.persist()
            flash('Your profile has been saved successfully.', 'success')
            return redirect(url_for('administrators.profile'))
        flash('Your profile has not been saved successfully.', 'danger')
    return render_template('administrators/views/profile.html', form=form)


@blueprint.route('/sign-in', methods=['GET', 'POST'])
def sign_in():
    if g.administrator:
        return redirect(
            request.args.get('next') or url_for('administrators.dashboard')
        )
    form = forms.sign_in(request.form)
    if request.method == 'POST':
        if form.validate_on_submit():
            flash('You have been signed in successfully.', 'success')
            return redirect(
                request.args.get('next') or url_for('administrators.dashboard')
            )
        flash('You have not been signed in successfully.', 'danger')
    return render_template('administrators/views/sign_in.html', form=form)


@blueprint.route('/sign-out')
def sign_out():
    if 'administrator' in session:
        del session['administrator']
    flash('You have been signed out successfully.', 'success')
    return redirect(url_for('administrators.dashboard'))
