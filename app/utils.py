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

import requests


def gen_records(**kwargs):
    """Fetches json from url"""
    for ind_id in kwargs['INDICATORS']:
        url = kwargs['BASE_URL'].format(ind_id)
        headers = {'Content-Type': 'application/json'}
        r = requests.get(url, headers=headers)

        country_names = r.json()['country_name']
        ind_name = r.json()['indicator_name']
        ind_values = r.json()['indicator_value']

        for country_code, ind_code, year, value in ind_values:
            record = {
                'indicator': ind_name[ind_code],
                'indicator_code': ind_code,
                'country_code': country_code,
                'country': country_names[country_code],
                'value': value,
                'year': year,
            }

            yield record

def fetch(**kwargs):
    return {'records': gen_records(**kwargs)}
