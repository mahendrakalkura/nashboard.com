# -*- coding: utf-8 -*-

from locale import LC_ALL, format, setlocale
from re import compile, IGNORECASE

from flask import request, session

setlocale(LC_ALL, 'en_US.UTF-8')

patterns = {
    'happy_hours': compile(
        'happy hour|drink deal|two for one|two-4-one|two-for-1|two-4-1|'
        'two-for-one|2-4-one|2-4-1|2-for-one|2-for-1|241|happy hr|happy hours|'
        'happy-hr|happy-hours|happy-hour|drink-deal',
        IGNORECASE
    ),
    'retweet': compile(' RT | RT @| RT@|^RT', IGNORECASE),
    'trivia': compile('trivia', IGNORECASE),
}


def get_filters_order_by_limit_page(table, filters, order_by, limit, page):
    if not table in session:
        session[table] = {}
    if 'filters' in session[table]:
        filters = session[table]['filters']
    if 'order_by' in session[table]:
        order_by = session[table]['order_by']
    if 'limit' in session[table]:
        limit = session[table]['limit']
    if 'page' in session[table]:
        page = session[table]['page']
    return filters, order_by, limit, page


def get_integer(value):
    return format('%d', value, grouping=True)


def set_filters(table, form):
    if not table in session:
        session[table] = {}
    if request.form.get('submit', default='') == 'set':
        session[table]['filters'] = form(request.form).data
        session[table]['page'] = 1
    if request.form.get('submit', default='') == 'unset':
        session[table]['filters'] = {}
        session[table]['page'] = 1


def set_order_by_limit_page(table):
    if not table in session:
        session[table] = {}
    if(
        'order_by_column' in request.args
        and
        'order_by_direction' in request.args
    ):
        session[table]['order_by'] = {
            'column': request.args['order_by_column'],
            'direction': request.args['order_by_direction'],
        }
    if 'limit' in request.args:
        session[table]['limit'] = int(request.args['limit'] or 0)
    if 'page' in request.args:
        session[table]['page'] = int(request.args['page'] or 0)


def is_happy_hour(category, text):
    if category == 'Happy Hours' and patterns['happy_hours'].search(text):
        return True
    return False


def is_retweet(text):
    if patterns['retweet'].search(text):
        return True
    return False


def is_trivia(category, text):
    if category == 'Trivia' and patterns['trivia'].search(text):
        return True
    return False
