from os import environ

DEBUG = True if environ.get('DEBUG', 'false').lower() == 'true' else False

APP_VERSION = environ.get('APP_VERSION')

LOG_LEVEL = environ.get('LOG_LEVEL', 'DEBUG')
