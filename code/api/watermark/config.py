import os
import logging
import sys
import uuid


class Config:
    CLIENT = str(uuid.uuid4())
    NAME = "{username}-{queue}".format(
        username=os.getenv('OS_USERNAME'),
        queue='watermark')

    OS_REGION_NAME = os.getenv('OS_REGION_NAME')
    OS_AUTH_URL = os.getenv('OS_AUTH_URL')
    OS_USERNAME = os.getenv('OS_USERNAME')
    OS_PASSWORD = os.getenv('OS_PASSWORD')

    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_RECORD_QUERIES = True

    SQLALCHEMY_DATABASE_URI = \
        '{engine}://{username}:{password}@{hostname}/{database}'.format(
            engine=os.getenv('WM_DB_ENGINE_DRIVER'),
            username=os.getenv('WM_DB_USERNAME'),
            password=os.getenv('WM_DB_PASSWORD'),
            hostname=os.getenv('WM_DB_HOSTNAME'),
            database=os.getenv('WM_DB_DATABASE'))

    ITEMS_PER_PAGE = 20
    SLOW_DB_QUERY_TIME = 0.5

    CONTAINER_CDN_URL = os.getenv('WM_CONTAINER_CDN_URL')

    @classmethod
    def init_app(cls, app):
        wm_logger = logging.getLogger('watermark')
        wm_logger.setLevel(logging.DEBUG)
        formatter = logging.Formatter(
            '%(asctime)s %(levelname)s: %(name)s %(message)s')

        stdout = logging.StreamHandler(sys.stdout)
        stdout.setFormatter(formatter)
        wm_logger.addHandler(stdout)

        file_handler = logging.FileHandler('wm_api.log')
        file_handler.setFormatter(formatter)
        wm_logger.addHandler(file_handler)



class DevelopmentConfig(Config):
    DEBUG = True


class TestingConfig(Config):
    TESTING = True


class ProductionConfig(Config):
    PRODUCTION = True

    @classmethod
    def init_app(cls, app):
        Config.init_app(app)

        from logging.handlers import SysLogHandler
        syslog_handler = SysLogHandler()
        syslog_handler.setLevel(logging.WARNING)
        app.logger.addHandler(syslog_handler)


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,

    'default': DevelopmentConfig
}