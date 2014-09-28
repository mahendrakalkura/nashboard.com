# -*- coding: utf-8 -*-

from flask import g
from sqlalchemy.orm import backref, relationship

from modules import database


class setting(database.base):
    __tablename__ = 'settings'
    __table_args__ = {
        'autoload': True,
    }


class category(database.base):
    __tablename__ = 'categories'
    __table_args__ = {
        'autoload': True,
    }

    def __init__(self, *args, **kwargs):
        super(category, self).__init__(*args, **kwargs)
        self.ttl = category.__table__.choices['ttl'][-1][0]

    def get_ttl(self):
        for key, value in category.__table__.choices['ttl']:
            if key == self.ttl:
                return value
        return ''

    def get_tweets(self):
        return g.mysql.query(
            tweet,
        ).join(
            handle,
        ).join(
            category_handle,
        ).filter(
            category_handle.category == self,
        ).count()

    def get_position(self):
        return g.mysql.query('position').from_statement(
            '''
            SELECT COALESCE(MAX(position), 0) + 1 AS position
            FROM categories
            '''
        ).one()[0]


    def set_position(self, direction):
        if direction == 'up':
            instance = g.mysql.query(
                category,
            ).filter(
                category.position < self.position
            ).order_by(
                'position desc'
            ).first()
            if instance:
                swap(self, instance)
        if direction == 'down':
            instance = g.mysql.query(
                category,
            ).filter(
                category.position > self.position
            ).order_by(
                'position asc'
            ).first()
            if instance:
                swap(self, instance)

category.__table__.choices = {
    'ttl': [
        (86400 * 1, '1 day'),
        (86400 * 2, '2 days'),
        (86400 * 3, '3 days'),
        (86400 * 4, '4 days'),
        (86400 * 5, '5 days'),
        (86400 * 6, '6 days'),
        (86400 * 7, '7 days'),
    ],
}


class handle(database.base):
    __tablename__ = 'handles'
    __table_args__ = {
        'autoload': True,
    }

    categories = relationship(
        'category',
        backref=backref('handles', lazy='dynamic'),
        lazy='dynamic',
        secondary='categories_handles'
    )


class category_handle(database.base):
    __tablename__ = 'categories_handles'
    __table_args__ = {
        'autoload': True,
    }

    category = relationship(
        'category',
        backref=backref(
            'categories_handles', cascade='all,delete-orphan', lazy='dynamic',
        ),
    )

    handle = relationship(
        'handle',
        backref=backref(
            'categories_handles', cascade='all,delete-orphan', lazy='dynamic',
        ),
    )


class tweet(database.base):
    __tablename__ = 'tweets'
    __table_args__ = {
        'autoload': True,
    }

    handle = relationship(
        'handle',
        backref=backref('tweets', cascade='all,delete-orphan', lazy='dynamic'),
    )


def swap(one, two):
    one.position, two.position = two.position, one.position
    g.mysql.add(one)
    g.mysql.add(two)
    g.mysql.commit()
