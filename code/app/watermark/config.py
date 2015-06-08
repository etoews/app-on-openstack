import os
import logging
import sys

class Config:
    TMP_DIR = '/tmp/app/'
    NAME = "{username}-{queue}".format(
        username=os.getenv('OS_USERNAME'),
        queue='watermark')

    OS_REGION_NAME = os.getenv('OS_REGION_NAME')
    OS_AUTH_URL = os.getenv('OS_AUTH_URL')
    OS_USERNAME = os.getenv('OS_USERNAME')
    OS_PASSWORD = os.getenv('OS_PASSWORD')

    API_SCHEME = os.getenv('WM_API_SCHEME')
    API_ENDPOINT = os.getenv('WM_API_ENDPOINT')

    API_URL = '{scheme}://{endpoint}'.format(
        scheme=API_SCHEME,
        endpoint=API_ENDPOINT
    )

    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

    @classmethod
    def init_app(cls, app):
        if not os.path.exists(cls.TMP_DIR):
            os.makedirs(cls.TMP_DIR)

        wm_logger = logging.getLogger('watermark')
        wm_logger.setLevel(logging.DEBUG)
        formatter = logging.Formatter(
            '%(asctime)s %(levelname)s: %(name)s %(message)s')

        stdout = logging.StreamHandler(sys.stdout)
        stdout.setFormatter(formatter)
        wm_logger.addHandler(stdout)

        file_handler = logging.FileHandler('wm_app.log')
        file_handler.setFormatter(formatter)
        wm_logger.addHandler(file_handler)

        wm_logger.debug("App ready")




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