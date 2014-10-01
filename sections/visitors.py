# -*- coding: utf-8 -*-

from bleach import linkify
from datetime import datetime, timedelta
from flask import (
    abort,
    Blueprint,
    flash,
    g,
    redirect,
    render_template,
    request,
    url_for
)
from pytz import utc

from modules import forms
from modules import models
from modules import utilities

blueprint = Blueprint('visitors', __name__)


@blueprint.route('/')
def dashboard():
    return render_template(
        'visitors/views/dashboard.html', categories=g.mysql.query(
            models.category,
        ).order_by('position asc').all()
    )


@blueprint.route('/ajax', methods=['POST'])
def ajax():
    category = g.mysql.query(models.category).get(request.form['id'])
    if not category:
        abort(404)
    counts = {}
    tweets = []
    for tweet in g.mysql.query(
        models.tweet,
    ).join(
        models.handle,
    ).join(
        models.category_handle,
    ).filter(
        models.category_handle.category == category,
        models.tweet.created_at >= datetime.now() - timedelta(seconds=category.ttl),
    ).order_by('created_at desc'):
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
        if not tweet.handle.screen_name in counts:
            counts[tweet.handle.screen_name] = 0
        if counts[tweet.handle.screen_name] >= 5:
            continue
        tweets.append({
            'created_at': tweet.created_at.replace(tzinfo=utc).isoformat(' '),
            'handle_profile_image_url': tweet.handle.profile_image_url,
            'handle_screen_name': tweet.handle.screen_name,
            'handle_name': tweet.handle.name,
            'id': tweet.id,
            'media': tweet.media,
            'text': linkify(tweet.text, [
                callback,
            ], parse_email=False, skip_pre=False),
        })
        counts[tweet.handle.screen_name] += 1
    return render_template('visitors/views/ajax.html', tweets=tweets)


@blueprint.route('/stay-in-touch', methods=['GET', 'POST'])
def stay_in_touch():
    visitor = models.visitor()
    form = forms.visitors_form(request.form, visitor)
    form.id = visitor.id
    if request.method == 'POST':
        if form.validate_on_submit():
            g.mysql.add(form.get_instance(visitor))
            g.mysql.commit()
            flash('You are subscribed successfully.', 'success')
            return redirect(url_for('visitors.dashboard'))
        flash('You are not subscribed.', 'danger')
    return render_template(
        'visitors/views/stay_in_touch.html', form=form,
    )


def callback(attrs, new=False):
    attrs['rel'] = 'nofollow'
    attrs['target'] = '_blank'
    return attrs
