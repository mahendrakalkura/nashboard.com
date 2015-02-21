# -*- coding: utf-8 -*-

from functools import wraps

from flask import g, redirect, request, session, url_for

from modules import log, timer


def profile(indent):
    def decorator(function):
        @wraps(function)
        def decorated_function(*args, **kwargs):
            log.write(10, '%(function)s()' % {
                'function': function.__name__
            }, indent)
            timer.start(function.__name__)
            output = function(*args, **kwargs)
            timer.stop(function.__name__)
            log.write(10, '%(seconds).3f seconds' % {
                'seconds': timer.get_seconds(function.__name__),
            }, indent)
            return output
        return decorated_function
    return decorator


def requires_administrator(function):
    @wraps(function)
    def decorated_function(*args, **kwargs):
        if g.administrator:
            return function(*args, **kwargs)
        if 'administrator' in session:
            del session['administrator']
        return redirect(url_for('administrators.sign_in', next=request.url))
    return decorated_function
