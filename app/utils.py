#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: sw=4:ts=4:expandtab

"""
utils
~~~~~

Provides miscellaneous utility methods
"""

from __future__ import (
    absolute_import, division, print_function, with_statement,
    unicode_literals)

import grequests

from datetime import datetime as dt
from ijson import items


def gen_data(start_year=None, end_year=None, **kwargs):
    """Generates historical or current data"""
    # url = 'file://%s' % p.join(_parentdir, 'data.json')
    end_year = int(end_year or dt.now().year)
    start_year = start_year or end_year - 1
    url = kwargs['BASE_URL']
    headers = {'Content-Type': 'application/json'}

    rs = [grequests.get(url, stream=True, headers=headers) for _ in xrange(3)]
    data = [r.raw for r in grequests.map(rs, stream=True, size=3)]

    country_names = items(data[0], kwargs['country_names']).next()
    ind_names = items(data[1], kwargs['ind_names']).next()
    ind_items = items(data[2], kwargs['ind_values'])

    for country_code, ind_code, year, ind_value in ind_items:
        year, ind_value = int(year), float(ind_value)

        if start_year and year < start_year:
            continue

        if end_year and year > end_year:
            continue

        record = {
            'rid': '%s-%s-%s' % (ind_code, country_code, year),
            'country': country_names[country_code],
            'indicator': ind_names[ind_code],
            'value': ind_value,
            'year': year,
        }

        yield record
