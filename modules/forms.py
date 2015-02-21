# -*- coding: utf-8 -*-

from bcrypt import gensalt, hashpw
from flask import g, session
from flask_wtf import Form
from wtforms.ext.sqlalchemy.fields import QuerySelectField, QuerySelectMultipleField
from wtforms.fields import PasswordField, SelectField, TextAreaField, TextField
from wtforms.widgets import CheckboxInput

from modules import models, validators, widgets


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
                hashpw(self.password.data.encode('utf-8'), password.encode('utf-8')) == password
            ):
                session['administrator'] = True
                return True
        self.username.errors = ['Invalid Username/Password']
        self.password.errors = []
        return False


class categories(Form):
    name = TextField(
        label='Name', validators=[validators.required(), validators.unique(table='categories', columns=[])],
    )
    ttl = SelectField(
        choices=models.category.__table__.choices['ttl'], coerce=int, label='TTL', validators=[validators.required()]
    )

    def get_instance(self, category):
        category.name = self.name.data
        category.ttl = self.ttl.data
        return category


class neighborhoods(Form):
    name = TextField(validators=[validators.required(), validators.unique(table='neighborhoods', columns=[])])

    def get_instance(self, neighborhood):
        neighborhood.name = self.name.data
        return neighborhood


class handles(Form):
    neighborhood = QuerySelectField(
        allow_blank=False,
        get_label='name',
        label='Neighborhood',
        query_factory=models.get_neighborhoods,
        validators=[validators.required()],
    )
    screen_name = TextField(
        label='Screen Name', validators=[validators.required(), validators.unique(table='handles', columns=[])],
    )
    name = TextField(label='Name', validators=[validators.required(), validators.unique(table='handles', columns=[])])
    profile_image_url = TextField(
        label='Profile Image URL', validators=[validators.required(), validators.unique(table='handles', columns=[])],
    )
    summary = TextAreaField(
        description=['Enter a brief summary of the handle...'],
        validators=[validators.required()],
        widget=widgets.textarea(rows=10),
    )
    categories = QuerySelectMultipleField(
        allow_blank=False,
        get_label='name',
        label='Categories',
        option_widget=CheckboxInput(),
        query_factory=models.get_categories,
        validators=[validators.required()],
        widget=widgets.list(prefix_label=False),
    )

    def get_instance(self, handle):
        handle.neighborhood = self.neighborhood.data
        handle.screen_name = self.screen_name.data
        handle.name = self.name.data
        handle.profile_image_url = self.profile_image_url.data
        handle.summary = self.summary.data
        handle.categories = self.categories.data
        return handle


class visitors(Form):
    email = TextField(validators=[
        validators.required(), validators.email(), validators.unique(table='visitors', columns=[]),
    ])

    def get_instance(self, visitor):
        visitor.email = self.email.data
        return visitor


class users_sign_up(Form):
    email = TextField(
        validators=[validators.required(), validators.email(), validators.unique(table='users', columns=[])]
    )
    password = PasswordField(validators=[validators.required()])
    confirm = PasswordField(label='Confirm Password', validators=[validators.required()])

    def validate(self):
        if super(users_sign_up, self).validate():
            if self.password.data == self.confirm.data:
                return True
            self.password.errors = [
                'password and confirm password are different',
            ]
            return False

    def get_instance(self, user):
        password = hashpw(self.password.data.encode('utf-8'), gensalt(10))
        user.email = self.email.data
        user.password = password
        return user


class users_sign_in(Form):
    email = TextField(validators=[validators.required(), validators.email()])
    password = PasswordField(validators=[validators.required()])

    def validate(self):
        if super(users_sign_in, self).validate():
            instance = g.mysql.query(
                models.user
            ).filter(
                models.user.email == self.email.data,
            ).first()
            if (
                instance
                and
                hashpw(self.password.data.encode('utf-8'), instance.password.encode('utf-8')) == instance.password
            ):
                session['visitor'] = instance.id
                return True
        self.email.errors = ['Invalid Username/Password']
        self.password.errors = []
        return False
