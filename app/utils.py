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

import time
import schedule as sch
import smtplib
import logging
import scraperwiki

from os import environ, path as p
from email.mime.text import MIMEText

from httplib import HTTPConnection
from ijson import items

_basedir = p.dirname(__file__)
_parentdir = p.dirname(_basedir)
_schedule_time = '10:30'
_recipient = 'reubano@gmail.com'

logging.basicConfig()
logger = logging.getLogger('hdxscraper-hdro')


def send_email(_to, _from=None, subject=None, text=None):
    user = environ.get('user')
    _from = _from or '%s@scraperwiki.com' % user
    subject = subject or 'scraperwiki box %s failed' % user
    text = text or 'https://scraperwiki.com/dataset/%s' % user
    msg = MIMEText(text)
    msg['Subject'], msg['From'], msg['To'] = subject, _from, _to

    # Send the message via our own SMTP server, but don't
    # include the envelope header.
    s = smtplib.SMTP('localhost')
    s.sendmail(_from, [_to], msg.as_string())
    s.quit()


def exception_handler(func):
    def wrapper(*args, **kwargs):
        try:
            func(*args, **kwargs)
        except Exception as e:
            logger.exception(str(e))
            scraperwiki.status('error', 'Error collecting data')

            with open(p.join(_parentdir, 'http', 'log.txt'), 'rb') as f:
                send_email(_recipient, text=f.read())
        else:
            scraperwiki.status('ok')

    return wrapper


def run_or_schedule(job, schedule=False, exception_handler=None):
    job()

    if schedule:
        job = exception_handler(job) if exception_handler else job
        sch.every(1).day.at(_schedule_time).do(job)

        while True:
            sch.run_pending()
            time.sleep(1)


def gen_data(config, start_year=None, end_year=None):
    """Generates historical or current data"""
    # url = 'file://%s' % p.join(_parentdir, 'data.json')
    url = config['BASE_URL']
    paths = config['DATA_LOCATIONS']
    conn = HTTPConnection(url.replace('http://', ''))

    conn.request('GET', '/')
    country_data = conn.getresponse()
    country_names = items(country_data, paths['country_names']).next()

    conn.request('GET', '/')
    ind_name_data = conn.getresponse()
    ind_names = items(ind_name_data, paths['ind_names']).next()

    conn.request('GET', '/')
    ind_value_data = conn.getresponse()
    ind_items = items(ind_value_data, paths['ind_values'])

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
