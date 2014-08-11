import os

basedir = os.path.abspath(os.path.dirname(__file__))

class BaseConfig(object):
    SECRET_KEY = os.environ.get('SECRET_KEY')
    ADMIN = os.environ.get('ADMIN')
    ADMIN_PASS = os.environ.get('ADMIN_PASS')

class DevelopmentConfig(BaseConfig):
    DEBUG = True
    SECRET_KEY = os.environ.get('SECRET_KEY') or 's3cr3t'
    SQLALCH_DB_URI = os.environ.get('DEV_DB_URI') or \
            'sqlite:///' + os.path.join(basedir, 'dev.sqlite')

class ProductionConfig(BaseConfig):
    DEBUG = False
    SQALCH_DB_URI = os.environ.get('DB_URI') or \
            'sqlite:///' + os.path.join(basedir, 'db.sqlite')

config = {
        'development' : DevelopmentConfig,
        'production' : ProductionConfig,
        'default' : DevelopmentConfig
    }
