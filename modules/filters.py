# -*- coding: utf-8 -*-

from flask_wtf import Form
from wtforms.fields import SelectField, TextField

from modules import models, validators


class handles(Form):
    screen_name = TextField(label='Screen Name')
    name = TextField(label='Name')
    category = SelectField(choices=[], default='')

    def __init__(self, *args, **kwargs):
        super(handles, self).__init__(*args, **kwargs)
        self.category.choices = [('', 'All')] + [(category.id, category.name) for category in models.get_categories()]

    def apply(self, query):
        if self.screen_name.data:
            query = query.filter(
                models.handle.screen_name.like('%%%(screen_name)s%%' % {
                    'screen_name': self.screen_name.data,
                })
            )
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


class visitors(Form):
    email = TextField(validators=[validators.required()])

    def apply(self, query):
        if self.email.data:
            query = query.filter(models.visitor.email.like('%%%(email)s%%' % {
                'email': self.email.data,
            }))
        return query
