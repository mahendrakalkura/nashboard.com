# -*- coding: utf-8 -*-

from datetime import datetime, timedelta
from difflib import SequenceMatcher

from authomatic.extras.flask import FlaskAuthomatic
from authomatic.providers import oauth1
from bleach import linkify
from flask import abort, Blueprint, flash, g, redirect, render_template, request, session, url_for
from pytz import utc

from modules import forms, models, utilities

from settings import DEBUG, SECRET_KEY, TWITTER_CONSUMER_KEY, TWITTER_CONSUMER_SECRET

blueprint = Blueprint('visitors', __name__)

twitter = FlaskAuthomatic(
    config={
        'twitter': {
            'class_': oauth1.Twitter,
            'consumer_key': TWITTER_CONSUMER_KEY,
            'consumer_secret': TWITTER_CONSUMER_SECRET,
        },
    },
    debug=DEBUG,
    secret=SECRET_KEY,
)


@blueprint.before_request
def before_request():
    g.categories = g.mysql.query(models.category).order_by('position asc').all()
    g.neighborhoods = g.mysql.query(models.neighborhood).order_by('position asc').all()
    g.user = None
    if 'user' in session:
        g.user = g.mysql.query(models.user).get(session['user'])


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
    neighborhood = g.mysql.query(models.neighborhood).get(request.form['neighborhood_id'])
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
    tweets = []
    counts = {}
    texts = []
    for tweet in query.order_by('created_at DESC , favorites DESC , retweets DESC'):
        vote = None
        if g.user:
            if vote:
                vote = vote.direction
            vote = g.mysql.query(
                models.vote,
            ).filter(
                models.vote.user_id == g.user.id,
                models.vote.tweet_id == tweet.id,
                models.vote.direction == 'up',
            ).first()
        votes = g.mysql.query(
            models.vote,
        ).filter(
            models.vote.tweet_id == tweet.id,
            models.vote.direction == 'up',
        ).count() - g.mysql.query(
            models.vote,
        ).filter(
            models.vote.tweet_id == tweet.id,
            models.vote.direction == 'down',
        ).count()
        score = votes + tweet.favorites + tweet.retweets
        if category.name == 'Happy Hours' and not utilities.is_happy_hour(category.name, tweet.text):
            continue
        if category.name == 'Trivia' and not utilities.is_trivia(category.name, tweet.text):
            continue
        if tweet.user_screen_name not in counts:
            counts[tweet.user_screen_name] = 0
        if counts[tweet.user_screen_name] >= 5:
            continue
        if category.name == 'Food & Beverage' or category.name == 'Music':
            text = len(filter(None, tweet.text.split(' ')))
            if text < 7:
                continue
            if tweet.text[0] == '"' or tweet.text[0] == '.':
                continue
            count = 0
            for text in texts:
                if get_ratio(text, tweet.text) > 0.67:
                    count += 1
            if count >= 1:
                continue
        tweets.append({
            'created_at': tweet.created_at.replace(tzinfo=utc).isoformat(' '),
            'favorites': tweet.favorites,
            'id': tweet.id,
            'media': tweet.media,
            'retweets': tweet.retweets,
            'score': score,
            'text': linkify(tweet.text, [callback], parse_email=False, skip_pre=False),
            'total_vote': total_vote,
            'user_name': tweet.user_name,
            'user_profile_image_url': tweet.user_profile_image_url,
            'user_screen_name': tweet.user_screen_name,
            'vote': vote,
            'votes': votes,
        })
        counts[tweet.user_screen_name] += 1
    if request.form['mode'] == 'whats_hot':
        tweets = sorted(
            tweets,
            key=lambda tweet: (
                -tweet['score'], -tweet['votes'], -tweet['created_at'], -tweet['favorites'], -tweet['retweets'],
            )
        )
    return render_template('visitors/views/dashboard_ajax.html', tweets=tweets)


@blueprint.route('/dashboard/vote', methods=['POST'])
def dashboard_vote():
    if not g.user:
        return ('', 204)
    vote = g.mysql.query(
        models.vote,
    ).filter(
        models.vote.user_id == g.user.id,
        models.vote.tweet_id == request.form['tweet_id'],
    ).first()
    if not vote:
        g.mysql.add(models.vote(**{
            'direction': request.form['direction'],
            'timestamp': datetime.now(),
            'tweet_id': request.form['tweet_id'],
            'user_id': g.user.id,
        }))
        g.mysql.commit()
    return ('', 204)


@blueprint.route('/handles/<screen_name>')
def handles(screen_name):
    handle = g.mysql.query(models.handle).filter(models.handle.screen_name == screen_name).first()
    if not handle:
        abort(404)
    return render_template('visitors/views/handles.html', handle=handle)


@blueprint.route('/handles/<screen_name>/ajax', methods=['POST'])
def handles_ajax(screen_name):
    handle = g.mysql.query(models.handle).filter(models.handle.screen_name == screen_name).first()
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
    for tweet in query.order_by('created_at DESC , favorites DESC, retweets DESC'):
        tweets.append({
            'created_at': tweet.created_at.replace(tzinfo=utc).isoformat(' '),
            'favorites': tweet.favorites,
            'id': tweet.id,
            'media': tweet.media,
            'retweets': tweet.retweets,
            'text': linkify(tweet.text, [callback], parse_email=False, skip_pre=False),
            'user_name': tweet.user_name,
            'user_profile_image_url': tweet.user_profile_image_url,
            'user_screen_name': tweet.user_screen_name,
        })
    return render_template('visitors/views/handles_ajax.html', tweets=tweets)


@blueprint.route('/users/sign-up', methods=['GET', 'POST'])
def users_sign_up():
    if g.user:
        return redirect(request.args.get('next') or url_for('visitors.dashboard'))
    user = models.user()
    form = forms.users_sign_up(request.form)
    form.id = user.id
    if form.validate_on_submit():
        g.mysql.add(form.get_instance(user))
        g.mysql.commit()
        flash('You have been signed up successfully.', 'success')
        return redirect(url_for('visitors.users_sign_in'))
    return render_template('visitors/views/users_sign_up.html', form=form)


@blueprint.route('/users/sign-up/twitter', methods=['GET', 'POST'])
@twitter.login('twitter')
def users_sign_up_twitter():
    if twitter.result:
        if twitter.result.error:
            flash(twitter.result.error.message, 'danger')
            return redirect(url_for('visitors.users_sign_up'))
        if twitter.result.user:
            if not (twitter.result.user.name and twitter.result.user.id):
                twitter.result.user.update()
            if not g.mysql.query(
                models.user,
            ).filter(
                models.user.twitter_screen_name == twitter.result.user.name,
            ).first():
                g.mysql.add(models.user(**{
                    'twitter_screen_name': twitter.result.user.name,
                }))
                g.mysql.commit()
            flash('You have been signed up successfully.', 'success')
            return redirect(url_for('visitors.users_sign_in'))
    return twitter.response


@blueprint.route('/users/sign-in', methods=['GET', 'POST'])
def users_sign_in():
    if g.user:
        return redirect(request.args.get('next') or url_for('visitors.dashboard'))
    form = forms.users_sign_in(request.form)
    if request.method == 'POST':
        if form.validate_on_submit():
            flash('You have been signed in successfully.', 'success')
            return redirect(request.args.get('next') or url_for('visitors.dashboard'))
        flash('You have not been signed in successfully.', 'danger')
    return render_template('visitors/views/users_sign_in.html', form=form)


@blueprint.route('/users/sign-in/twitter', methods=['GET', 'POST'])
@twitter.login('twitter')
def users_sign_in_twitter():
    if twitter.result:
        if twitter.result.error:
            flash(twitter.result.error.message, 'danger')
            return redirect(url_for('visitors.users_sign_up'))
        if twitter.result.user:
            if not (twitter.result.user.name and twitter.result.user.id):
                twitter.result.user.update()
            instance = g.mysql.query(
                models.user,
            ).filter(
                models.user.twitter_screen_name == twitter.result.user.name,
            ).first()
            if not instance:
                flash('You have not been signed in successfully.', 'danger')
                return redirect(url_for('visitors.users_sign_in'))
            session['visitor'] = instance.id
            flash('You have been signed in successfully.', 'success')
            return redirect(url_for('visitors.dashboard'))
    return twitter.response


@blueprint.route('/users/sign-out')
def users_sign_out():
    if 'user' in session:
        del session['user']
    flash('You have been signed out successfully.', 'success')
    return redirect(url_for('visitors.users_sign_in'))


@blueprint.route('/stay-in-touch', methods=['GET', 'POST'])
def stay_in_touch():
    visitor = models.visitor()
    form = forms.visitors(request.form, visitor)
    form.id = visitor.id
    if request.method == 'POST':
        if form.validate_on_submit():
            g.mysql.add(form.get_instance(visitor))
            g.mysql.commit()
            flash('You have been subscribed successfully.', 'success')
            return redirect(url_for('visitors.stay_in_touch'))
        flash('You have not been subscribed successfully.', 'success')
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
