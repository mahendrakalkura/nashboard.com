# -*- coding: utf-8 -*-

from logging import getLogger
from pprint import pprint

from flask.ext.script import Manager
from webassets.script import CommandLineEnvironment

from modules import decorators
from modules import twitter

from server import application, assets

manager = Manager(application, with_default_commands=False)


@manager.command
@decorators.profile(0)
def assets_():
    CommandLineEnvironment(assets, getLogger('flask')).build()


@manager.command
@decorators.profile(0)
def twitter_process():
    twitter.process()


@manager.command
@decorators.profile(0)
def twitter_test():
    pprint(twitter.test())

if __name__ == '__main__':
    manager.run()
