from secrets import token_urlsafe

# Basic Config
class Config(object):
    DEBUG = True
    HOST = '127.0.0.1'
    SECRET_KEY = token_urlsafe(16)
    SESSION_COOKIE_SECURE = False

