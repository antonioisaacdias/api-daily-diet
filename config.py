import os

class Config:
    SQLALCHEMY_DATABASE_URI = 'sqlite:///daily_diet.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.urandom(24)