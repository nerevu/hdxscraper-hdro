from os import path as p

# module vars
_basedir = p.dirname(__file__)
_parentdir = p.dirname(_basedir)
_db_name = 'scraperwiki.sqlite'


# configuration
class Config(object):
    BASE_URL = 'http://ec2-52-1-168-42.compute-1.amazonaws.com'
    DATA_LOCATIONS = {
        'country_names': 'country_name',
        'ind_values': 'indicator_value.item',
        'ind_names': 'indicator_name',
    }

    SQLALCHEMY_DATABASE_URI = 'sqlite:///%s' % p.join(_basedir, _db_name)
    TABLE = 'HDRO'
    RECORD_ID = 'rid'
    SW = False
    DEBUG = False
    TESTING = False
    PROD = False
    CHUNK_SIZE = 2 ** 14
    ROW_LIMIT = None


class Scraper(Config):
    PROD = True
    SW = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///%s' % p.join(_parentdir, _db_name)


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
