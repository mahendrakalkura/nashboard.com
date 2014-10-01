# -*- coding: utf-8 -*-

from flask import g
from wtforms.compat import string_types
from wtforms.validators import (
    DataRequired,
    Email,
    StopValidation,
    ValidationError
)

from modules import database


class email(Email):

    def __init__(self, *args, **kwargs):
        self.message = 'Invalid Email'
        super(email, self).__init__(*args, **kwargs)


class required(DataRequired):
    field_flags = ('required', )

    def __call__(self, form, field):
        if (
            not field.data
            or
            (isinstance(field.data, string_types) and not field.data.strip())
        ):
            field.errors[:] = []
            raise StopValidation('Invalid %(text)s' % {
                'text': field.label.text,
            })


class unique(object):

    def __init__(self, table, columns):
        self.table = table
        self.columns = columns

    def __call__(self, form, field):
        table = database.base.metadata.tables[self.table]
        query = g.mysql.query(table)
        query = query.filter(getattr(table.c, field.id) == field.data)
        query = query.filter(getattr(table.c, 'id') != form.id)
        for column in self.columns:
            query = query.filter(
                getattr(table.c, column) == getattr(form, column)
            )
        if query.count():
            raise ValidationError(u'Duplicate %(label)s' % {
                'label': field.label.text
            })
