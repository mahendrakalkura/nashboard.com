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
def ajax():
    category = g.mysql.query(models.category).get(request.form['category_id'])
    if not category:
        abort(404)
    query = g.mysql.query(
        models.tweet,
    ).join(
        models.handle,
    ).join(
        models.category_handle,
    ).filter(
        models.category_handle.category == category,
        models.tweet.created_at
        >=
        datetime.now() - timedelta(seconds=category.ttl),
    )
    neighborhood = g.mysql.query(
        models.neighborhood,
    ).get(request.form['neighborhood_id'])
    if neighborhood:
        query = query.filter(models.handle.neighborhood_id == neighborhood.id)
    counts = {}
    tweets = []
    for tweet in query.order_by(
        'favorites desc, retweets desc, created_at desc'
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
        if not tweet.handle.screen_name in counts:
            counts[tweet.handle.screen_name] = 0
        if counts[tweet.handle.screen_name] >= 5:
            continue
        tweets.append({
            'created_at': tweet.created_at.replace(tzinfo=utc).isoformat(' '),
            'favorites': tweet.favorites,
            'handle_profile_image_url': tweet.handle.profile_image_url,
            'handle_screen_name': tweet.handle.screen_name,
            'handle_name': tweet.handle.name,
            'id': tweet.id,
            'media': tweet.media,
            'retweets': tweet.retweets,
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
            flash('You have been subscribed successfully.', 'success')
            return redirect(url_for('visitors.stay_in_touch'))
        flash('There was a problem..', 'danger')
    if request.args.get('f'):
        flash("We're still under development! Check back later for updates!",'warning')

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
