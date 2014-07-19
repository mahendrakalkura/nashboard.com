# -*- coding: utf-8 -*-

from datetime import datetime
from os.path import abspath, dirname, join

from flask import Flask, g, redirect, send_from_directory, session, url_for
from flask.ext.assets import Bundle, Environment

from modules import database
from modules import utilities

from sections import administrators
from sections import others
from sections import visitors

application = Flask(
    __name__, static_folder=join(abspath(dirname(__file__)), 'resources')
)
application.config.from_pyfile('settings.py')
application.jinja_env.add_extension('jinja2.ext.do')
application.jinja_env.add_extension('jinja2.ext.loopcontrols')
application.jinja_env.add_extension('jinja2.ext.with_')
application.register_blueprint(
    administrators.blueprint, url_prefix='/administrators'
)
application.register_blueprint(others.blueprint, url_prefix='/others')
application.register_blueprint(visitors.blueprint)


def url_for_(rule, **kwargs):
    kwargs.setdefault('_external', True)
    return url_for(rule, **kwargs)

application.jinja_env.globals['url_for'] = url_for_

assets = Environment(application)
assets.cache = False
assets.debug = application.config['DEBUG']
assets.directory = application.static_folder
assets.manifest = 'json:assets/versions.json'
assets.url = application.static_url_path
assets.url_expire = True
assets.versions = 'hash'
assets.register('javascripts', Bundle(
    'vendor/jquery/dist/jquery.js',
    'vendor/jquery-backstretch/jquery.backstretch.js',
    'vendor/jquery-timeago/jquery.timeago.js',
    'vendor/bootstrap/dist/js/bootstrap.js',
    'vendor/lightbox2/js/lightbox.js',
    'javascripts/all.js',
    filters='rjsmin' if not application.config['DEBUG'] else None,
    output='assets/compressed.js',
))
assets.register('stylesheets', Bundle(
    'vendor/lightbox2/css/lightbox.css',
    Bundle(
        'stylesheets/all.less',
        filters='less',
        output='stylesheets/all.css',
    ),
    filters='cssmin,cssrewrite'if not application.config['DEBUG'] else None,
    output='assets/compressed.css',
))


@application.before_request
def before_request():
    g.mysql = database.session()
    g.year = datetime.now().strftime('%Y')
    session.permanent = True


@application.after_request
def after_request(response):
    g.mysql.close()
    return response


@application.route('/')
def dashboard():
    return redirect(url_for('visitors.dashboard'))


@application.route('/404')
@application.errorhandler(404)
def errors_404(error=None):
    return others.errors_404(error)


@application.route('/500')
@application.errorhandler(500)
def errors_500(error=None):
    return others.errors_500(error)


@application.route('/favicon.ico')
def favicon():
    return send_from_directory(join(
        application.root_path, 'resources', 'images'
    ), 'favicon.ico')


@application.template_filter('format_integer')
def format_integer(value):
    return utilities.get_integer(value)


if __name__ == '__main__':
    application.run()
