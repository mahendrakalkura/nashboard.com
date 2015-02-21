# -*- coding: utf-8 -*-

from contextlib import closing
from datetime import datetime, timedelta
from logging import getLogger
from pprint import pprint

from celery import Celery
from flask.ext.script import Manager
from webassets.script import CommandLineEnvironment

from modules import database
from modules import decorators
from modules import log
from modules import models
from modules import twitter
from modules import utilities

from server import application, assets
from settings import BROKER


celery = Celery('manager')
celery.conf.update(
    BROKER=BROKER,
    BROKER_POOL_LIMIT=0,
    CELERY_ACCEPT_CONTENT=['json'],
    CELERY_ACKS_LATE=True,
    CELERY_IGNORE_RESULT=True,
    CELERY_RESULT_SERIALIZER='json',
    CELERY_TASK_SERIALIZER='json',
    CELERYD_LOG_FORMAT='[%(asctime)s: %(levelname)s] %(message)s',
    CELERYD_POOL_RESTARTS=True,
    CELERYD_PREFETCH_MULTIPLIER=1,
    CELERYD_TASK_SOFT_TIME_LIMIT=3600,
    CELERYD_TASK_TIME_LIMIT=7200,
)

manager = Manager(application, with_default_commands=False)


@celery.task
def twitter_1(id):
    log.write(10, id, 1)
    with closing(database.session()) as session:
        handle = session.query(models.handle).get(id)
        log.write(10, handle.screen_name, 1)
        tweets = []
        for tweet in twitter.get_tweets('from:%(screen_name)s' % {
            'screen_name': handle.screen_name,
        }):
            tweets.append(tweet)
        for tweet in twitter.get_tweets('@%(screen_name)s' % {
            'screen_name': handle.screen_name,
        }):
            tweets.append(tweet)
        seven_days_ago = datetime.now() - timedelta(days=7)
        for tweet in tweets:
            if tweet['text'].startswith('@'):
                continue
            if tweet['text'].startswith('I posted'):
                continue
            if utilities.is_retweet(tweet['text']):
                continue
            if tweet['created_at'] <= seven_days_ago:
                continue
            instance = session.query(models.tweet).get(tweet['id'])
            if not instance:
                instance = models.tweet(**{
                    'id': tweet['id'],
                })
            instance.created_at = tweet['created_at']
            instance.favorites = tweet['favorites']
            instance.media = tweet['media']
            instance.retweets = tweet['retweets']
            instance.text = tweet['text']
            instance.user_name = tweet['user_name']
            instance.user_profile_image_url = tweet['user_profile_image_url']
            instance.user_screen_name = tweet['user_screen_name']
            session.add(instance)
            session.commit()
            session.refresh(handle)
        log.write(10, len(tweets), 2)


@manager.command
@decorators.profile(0)
def assets_():
    CommandLineEnvironment(assets, getLogger('flask')).build()


@manager.command
@decorators.profile(0)
def process_1():
    with closing(database.session()) as session:
        for handle in session.query(models.handle).order_by('id ASC').all():
            twitter_1.delay(handle.id)


@manager.command
@decorators.profile(0)
def process_2():
    with closing(database.session()) as session:
        session.query(
            models.tweet,
        ).filter(
            models.tweet.created_at <= datetime.now() - timedelta(days=7),
        ).delete(
            synchronize_session=False,
        )
        session.commit()


@manager.command
@decorators.profile(0)
def twitter_2():
    pprint(twitter.get_tweets('from:NashFoodTrucks'))

if __name__ == '__main__':
    manager.run()
