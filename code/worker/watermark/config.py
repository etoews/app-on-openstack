import os
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

    API_SCHEME = os.getenv('WM_API_SCHEME')
    API_ENDPOINT = os.getenv('WM_API_ENDPOINT')

    API_URL = '{scheme}://{endpoint}'.format(
        scheme=API_SCHEME,
        endpoint=API_ENDPOINT
    )

class DevelopmentConfig(Config):
    DEBUG = True
    API_SCHEME = "http"
    API_ENDPOINT = "127.0.0.1:5000"


class TestingConfig(Config):
    TESTING = True


class ProductionConfig(Config):
    PRODUCTION = True


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,

    'default': DevelopmentConfig
}
