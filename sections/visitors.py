# -*- coding: utf-8 -*-

from datetime import datetime, timedelta
from difflib import SequenceMatcher
from re import compile, match

from bleach import linkify
from flask import (
    abort, Blueprint, flash, g, redirect, render_template, request, url_for,
)
from pytz import utc

from modules import forms
from modules import models
from modules import utilities

blueprint = Blueprint('visitors', __name__)


@blueprint.before_request
def before_request():
    g.categories = g.mysql.query(
        models.category,
    ).order_by('position asc').all()
    g.neighborhoods = g.mysql.query(
        models.neighborhood,
    ).order_by('position asc').all()


@blueprint.route('/')
def dashboard():
    return render_template('visitors/views/dashboard.html')


@blueprint.route('/ajax', methods=['POST'])
def dashboard_ajax():
    category = g.mysql.query(models.category).get(request.form['category_id'])
    if not category:
        abort(404)
    screen_names = []
    query = g.mysql.query(
        models.handle,
    ).join(
        models.category_handle,
    ).filter(
        models.category_handle.category == category,
    )
    neighborhood = g.mysql.query(
        models.neighborhood,
    ).get(request.form['neighborhood_id'])
    if neighborhood:
        query = query.filter(models.handle.neighborhood_id == neighborhood.id)
    for handle in query.all():
        screen_names.append(handle.screen_name)
    query = g.mysql.query(
        models.tweet,
    ).filter(
        models.tweet.user_screen_name.in_(screen_names),
        models.tweet.created_at
        >=
        datetime.now() - timedelta(seconds=category.ttl),
    )
    counts = {}
    tweets = []
    texts = []
    for tweet in query.order_by(
        'created_at asc, favorites desc, retweets desc',
    ):
        if (
            category.name == 'Happy Hours'
            and
            not utilities.is_happy_hour(category.name, tweet.text)
        ):
            continue
        if (
            category.name == 'Trivia'
            and
            not utilities.is_trivia(category.name, tweet.text)
        ):
            continue
        if not tweet.user_screen_name in counts:
            counts[tweet.user_screen_name] = 0
        if counts[tweet.user_screen_name] >= 5:
            continue
        if (
            category.name == 'Food & Beverage'
            or
            category.name == 'Music'
        ):
            text = len(filter(None, tweet.text.split(' ')))
            if text < 7:
                continue
            if (
                tweet.text[0] == '"'
                or
                tweet.text[0] == '.'
            ):
                continue
            count = 0
            for text in texts:
                if get_ratio(text, tweet.text) > 0.67:
                    count += 1
            if count >= 1:
                continue
            tweets.append({
                'created_at': tweet.created_at.replace(
                    tzinfo=utc
                ).isoformat(' '),
                'favorites': tweet.favorites,
                'id': tweet.id,
                'media': tweet.media,
                'retweets': tweet.retweets,
                'text': linkify(tweet.text, [
                    callback,
                ], parse_email=False, skip_pre=False),
                'user_name': tweet.user_name,
                'user_profile_image_url': tweet.user_profile_image_url,
                'user_screen_name': tweet.user_screen_name,
            })
            texts.append(tweet.text)
        else:
            tweets.append({
                'created_at': tweet.created_at.replace(
                    tzinfo=utc
                ).isoformat(' '),
                'favorites': tweet.favorites,
                'id': tweet.id,
                'media': tweet.media,
                'retweets': tweet.retweets,
                'text': linkify(tweet.text, [
                    callback,
                ], parse_email=False, skip_pre=False),
                'user_name': tweet.user_name,
                'user_profile_image_url': tweet.user_profile_image_url,
                'user_screen_name': tweet.user_screen_name,
            })
        counts[tweet.user_screen_name] += 1
    return render_template(
        'visitors/views/dashboard_ajax.html', tweets=reversed(tweets),
    )


@blueprint.route('/handles/<screen_name>')
def handles(screen_name):
    handle = g.mysql.query(
        models.handle,
    ).filter(
        models.handle.screen_name == screen_name,
    ).first()
    if not handle:
        abort(404)
    return render_template('visitors/views/handles.html', handle=handle)


@blueprint.route('/handles/<screen_name>/ajax', methods=['POST'])
def handles_ajax(screen_name):
    handle = g.mysql.query(
        models.handle,
    ).filter(
        models.handle.screen_name == screen_name,
    ).first()
    if not handle:
        abort(404)
    query = g.mysql.query(
        models.tweet,
    ).filter(
        models.tweet.text.like('%%@%(screen_name)s%%' % {
            'screen_name': handle.screen_name,
        }),
        models.tweet.created_at <= datetime.now(),
    )
    tweets = []
    for tweet in query.order_by(
        'favorites desc, retweets desc, created_at desc'
    ):
        tweets.append({
            'created_at': tweet.created_at.replace(tzinfo=utc).isoformat(' '),
            'favorites': tweet.favorites,
            'id': tweet.id,
            'media': tweet.media,
            'retweets': tweet.retweets,
            'text': linkify(tweet.text, [
                callback,
            ], parse_email=False, skip_pre=False),
            'user_name': tweet.user_name,
            'user_profile_image_url': tweet.user_profile_image_url,
            'user_screen_name': tweet.user_screen_name,
        })
    return render_template('visitors/views/handles_ajax.html', tweets=tweets)


@blueprint.route('/stay-in-touch', methods=['GET', 'POST'])
def stay_in_touch():
    visitor = models.visitor()
    form = forms.visitors_form(request.form, visitor)
    form.id = visitor.id
    if request.method == 'POST':
        if form.validate_on_submit():
            g.mysql.add(form.get_instance(visitor))
            g.mysql.commit()
            flash('You have been subscribed successfully.', 'success')
            return redirect(url_for('visitors.stay_in_touch'))
        flash('There was a problem..', 'danger')
    if request.args.get('f'):
        flash(
            "We're still under development! Check back later for updates!",
            'warning'
        )
    return render_template('visitors/views/stay_in_touch.html', form=form)


@blueprint.route('/privacy-policy')
def privacy_policy():
    return render_template('visitors/views/privacy_policy.html')


@blueprint.route('/about')
def about():
    return render_template('visitors/views/about.html')


def callback(attrs, new=False):
    attrs['rel'] = 'nofollow'
    attrs['target'] = '_blank'
    return attrs


def get_ratio(a, b):
    return SequenceMatcher(None, a, b).ratio()
