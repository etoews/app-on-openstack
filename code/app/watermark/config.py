import os


class Config:
    API_SCHEME = os.getenv('WM_API_SCHEME')
    API_ENDPOINT = os.getenv('WM_API_ENDPOINT')

    @classmethod
    def init_app(cls, app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True
    API_SCHEME = "http"
    API_ENDPOINT = "127.0.0.1:5000"


class TestingConfig(Config):
    TESTING = True
    WTF_CSRF_ENABLED = False


class ProductionConfig(Config):
    PRODUCTION = True


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