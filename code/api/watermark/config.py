import os


class Config:
    SECRET_KEY = os.environ.get('WM_SECRET_KEY') or 'hard to guess string'
    SSL_DISABLE = False

    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get('WM_MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('WM_MAIL_PASSWORD')

    WM_MAIL_SUBJECT_PREFIX = '[Flasky]'
    WM_MAIL_SENDER = 'Flasky Admin <flasky@example.com>'
    WM_ADMIN = os.environ.get('WM_ADMIN')

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
    def init_api(cls, api):
        pass


class DevelopmentConfig(Config):
    DEBUG = True


class TestingConfig(Config):
    TESTING = True


class ProductionConfig(Config):
    @classmethod
    def init_api(cls, api):
        Config.init_api(api)

        # email errors to the administrators
        import logging
        from logging.handlers import SMTPHandler
        credentials = None
        secure = None
        if getattr(cls, 'MAIL_USERNAME', None) is not None:
            credentials = (cls.MAIL_USERNAME, cls.MAIL_PASSWORD)
            if getattr(cls, 'MAIL_USE_TLS', None):
                secure = ()
        mail_handler = SMTPHandler(
            mailhost=(cls.MAIL_SERVER, cls.MAIL_PORT),
            fromaddr=cls.FLASKY_MAIL_SENDER,
            toaddrs=[cls.FLASKY_ADMIN],
            subject=cls.FLASKY_MAIL_SUBJECT_PREFIX + ' Application Error',
            credentials=credentials,
            secure=secure)
        mail_handler.setLevel(logging.ERROR)
        app.logger.addHandler(mail_handler)


class UnixConfig(ProductionConfig):
    @classmethod
    def init_api(cls, api):
        ProductionConfig.init_api(api)

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