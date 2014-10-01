# -*- coding: utf-8 -*-

from bcrypt import gensalt, hashpw
from flask import g, session
from flask_wtf import Form
from wtforms.ext.sqlalchemy.fields import (
    QuerySelectField, QuerySelectMultipleField,
)
from wtforms.fields import (
    PasswordField,
    SelectField,
    TextAreaField,
    TextField,
)
from wtforms.widgets import CheckboxInput

from modules import models
from modules import validators
from modules import widgets


def get_categories_factory():
    return g.mysql.query(models.category).order_by('position asc').all()


def get_neighborhoods_factory():
    return g.mysql.query(models.neighborhood).order_by('position asc').all()


class categories_form(Form):
    name = TextField(
        label='Name',
        validators=[
            validators.required(),
            validators.unique(table='categories', columns=[]),
        ],
    )
    ttl = SelectField(
        choices=models.category.__table__.choices['ttl'],
        coerce=int,
        label='TTL',
        validators=[
            validators.required(),
        ]
    )

    def get_instance(self, category):
        category.name = self.name.data
        category.ttl = self.ttl.data
        return category


class handles_form(Form):
    neighborhood = QuerySelectField(
        allow_blank=False,
        get_label='name',
        label='Neighborhood',
        query_factory=get_neighborhoods_factory,
        validators=[
            validators.required(),
        ],
    )
    name = TextField(
        label='Name',
        validators=[
            validators.required(),
            validators.unique(table='handles', columns=[]),
        ],
    )
    summary = TextAreaField(
        default='A brief summary of the handle.....',
        validators=[validators.required()],
        widget=widgets.textarea(rows=10),
    )
    categories = QuerySelectMultipleField(
        allow_blank=False,
        get_label='name',
        label='Categories',
        option_widget=CheckboxInput(),
        query_factory=get_categories_factory,
        validators=[validators.required()],
        widget=widgets.list(prefix_label=False),
    )

    def get_instance(self, handle):
        handle.neighborhood = self.neighborhood.data
        handle.name = self.name.data
        handle.categories = self.categories.data
        handle.summary = self.summary.data
        return handle


class handles_filters(Form):
    name = TextField(label='Name')
    category = SelectField(choices=[], default='')

    def __init__(self, *args, **kwargs):
        super(handles_filters, self).__init__(*args, **kwargs)
        self.category.choices = [('', 'All')] + [
            (category.id, category.name)
            for category in get_categories_factory()
        ]

    def apply(self, query):
        if self.name.data:
            query = query.filter(
                models.handle.name.like('%%%(name)s%%' % {
                    'name': self.name.data,
                })
            )
        if self.category.data:
            query = query.join(
                models.category_handle,
            ).join(
                models.category,
            ).filter(
                models.category.id == self.category.data,
            )
        return query


class neighborhoods_form(Form):
    name = TextField(validators=[
        validators.required(),
        validators.unique(table='neighborhoods', columns=[]),
    ])

    def get_instance(self, neighborhood):
        neighborhood.name = self.name.data
        return neighborhood


class profile(Form):
    username = TextField(validators=[validators.required()])
    password = PasswordField(validators=[validators.required()])

    def persist(self):
        g.mysql.query(
            models.setting,
        ).filter(
            models.setting.key == 'username',
        ).update({
            'value': self.username.data,
        })
        g.mysql.commit()
        g.mysql.query(
            models.setting,
        ).filter(
            models.setting.key == 'password',
        ).update({
            'value': hashpw(self.password.data.encode('utf-8'), gensalt(10)),
        })
        g.mysql.commit()


class sign_in(Form):
    username = TextField(validators=[validators.required()])
    password = PasswordField(validators=[validators.required()])

    def validate(self):
        if super(sign_in, self).validate():
            username = g.mysql.query(
                models.setting,
            ).filter(
                models.setting.key == 'username',
            ).first().value
            password = g.mysql.query(
                models.setting,
            ).filter(
                models.setting.key == 'password',
            ).first().value
            if (
                username == self.username.data
                and
                hashpw(self.password.data.encode('utf-8'), password.encode('utf-8'))
                ==
                password
            ):
                session['administrator'] = True
                return True
        self.username.errors = ['Invalid Username/Password']
        self.password.errors = []
        return False


class visitors_form(Form):
    email = TextField(validators=[
        validators.required(),
        validators.email(),
        validators.unique(table='visitors', columns=[]),
    ])

    def get_instance(self, visitor):
        visitor.email = self.email.data
        return visitor


class visitors_filters(Form):
    email = TextField(validators=[
        validators.required(),
    ])

    def apply(self, query):
        if self.email.data:
            query = query.filter(models.visitor.email.like('%%%(email)s%%' % {
                'email': self.email.data,
            }))
        return query
