# -*- coding: utf-8 -*-

from flask import Blueprint, render_template

blueprint = Blueprint('others', __name__)


@blueprint.route('/404')
def errors_404(error=None):
    return render_template('others/views/404.html'), 404


@blueprint.route('/500')
def errors_500(error=None):
    return render_template('others/views/500.html'), 500
