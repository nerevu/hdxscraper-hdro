# -*- coding: utf-8 -*-
"""
    app.models
    ~~~~~~~~~~

    Provides the SQLAlchemy models
"""
from __future__ import (
    absolute_import, division, print_function, with_statement,
    unicode_literals)

import savalidation.validators as val

from datetime import datetime as dt
from app import db
from savalidation import ValidationMixin


class HDRO(db.Model, ValidationMixin):
    # auto keys
    id = db.Column(db.Integer, primary_key=True)
    utc_created = db.Column(db.DateTime, nullable=False, default=dt.utcnow())
    utc_updated = db.Column(
        db.DateTime, nullable=False, default=dt.utcnow(), onupdate=dt.utcnow())

    # other keys
    rid = db.Column(db.String(16), nullable=False, index=True)
    country = db.Column(db.String(32), nullable=False)
    indicator = db.Column(db.String(128), nullable=False)
    value = db.Column(db.Numeric, nullable=False)
    year = db.Column(db.Integer, nullable=False)

    # validation
    val.validates_constraints()

    def __repr__(self):
        return ('<HDRO(%r, %r)>' % (self.country, self.indicator))
