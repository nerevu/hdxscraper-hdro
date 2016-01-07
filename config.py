# -*- coding: utf-8 -*-
# vim: sw=4:ts=4:expandtab

"""
config
~~~~~~

Provides app configuration settings
"""

from __future__ import (
    absolute_import, division, print_function, with_statement,
    unicode_literals)

from os import path as p

BASEDIR = p.dirname(__file__)
PARENTDIR = p.dirname(BASEDIR)
DB_NAME = 'scraperwiki.sqlite'
RECIPIENT = 'reubano@gmail.com'


class Config(object):
    BASE_URL = 'http://ec2-52-1-168-42.compute-1.amazonaws.com/version/1/indicator_id/{}'
    KEY = 'indicator'
    INDICATORS = [137506, 138806, 68606, 137906, 38406, 72206, 53906, 103706, 101006]
    SQLALCHEMY_DATABASE_URI = 'sqlite:///%s' % p.join(BASEDIR, DB_NAME)
    LOGFILE = p.join(BASEDIR, 'http', 'log.txt')
    API_LIMIT = 1000
    SW = False
    DEBUG = False
    TESTING = False
    PROD = False
    CHUNK_SIZE = 2 ** 14
    ROW_LIMIT = None


class Scraper(Config):
    PROD = True
    SW = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///%s' % p.join(PARENTDIR, DB_NAME)
    LOGFILE = p.join(PARENTDIR, 'http', 'log.txt')


class Production(Config):
    PROD = True


class Development(Config):
    DEBUG = True
    ROW_LIMIT = 50


class Test(Config):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    DEBUG = True
    ROW_LIMIT = 10
    TESTING = True
