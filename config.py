import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
  DEBUG = False
  TESTING = False
  CSRF_ENABLED = True
  SECRET_KEY = 'Fn9kmuYCbgodkUoYgsmWKgSg5t7zjQqLyX6f2sHAey4SC2ukfo4Rjw4aJFxGQhL6'
  SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'data.sqlite')
  SQLALCHEMY_TRACK_MODIFICATIONS = False
  RIOT_API_KEY = 'RGAPI-c8858b71-bace-4366-8bbe-eafbfc6b39e9'
                                