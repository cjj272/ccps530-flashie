import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
  DEBUG = False
  TESTING = False
  CSRF_ENABLED = True
  SECRET_KEY = 'CHANGE_THIS_TO_SOMETHING_MORE_SECURE'
  SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'data.sqlite')
  SQLALCHEMY_TRACK_MODIFICATIONS = False
                
