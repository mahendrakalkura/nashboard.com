# -*- coding: utf-8 -*-

from logging import getLogger

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
def twitter_():
    twitter.process()


if __name__ == '__main__':
    manager.run()
