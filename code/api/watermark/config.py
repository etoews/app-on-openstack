import os


class Config:
    SECRET_KEY = os.environ.get('WM_SECRET_KEY') or 'hard to guess string'
    SSL_DISABLE = False

    ITEMS_PER_PAGE = 20
    SLOW_DB_QUERY_TIME = 0.5

    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_RECORD_QUERIES = True

    SQLALCHEMY_DATABASE_URI = \
        '{engine}://{username}:{password}@{hostname}/{database}'.format(
            engine=os.getenv('WM_DB_ENGINE_DRIVER'),
            username=os.getenv('WM_DB_USERNAME'),
            password=os.getenv('WM_DB_PASSWORD'),
            hostname=os.getenv('WM_DB_HOSTNAME'),
            database=os.getenv('WM_DB_DATABASE'))

    @classmethod
    def init_app(cls, app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True


class TestingConfig(Config):
    TESTING = True


class ProductionConfig(Config):
    PRODUCTION = True

    @classmethod
    def init_app(cls, app):
        Config.init_app(app)


class UnixConfig(ProductionConfig):
    @classmethod
    def init_app(cls, app):
        ProductionConfig.init_app(app)

        # log to syslog
        import logging
        from logging.handlers import SysLogHandler
        syslog_handler = SysLogHandler()
        syslog_handler.setLevel(logging.WARNING)
        app.logger.addHandler(syslog_handler)


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'unix': UnixConfig,

    'default': DevelopmentConfig
}