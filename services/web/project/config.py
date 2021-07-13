"""Configuration of app"""
import os


basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    """Config for db, static folder, restplus"""
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "postgresql://")
    STATIC_FOLDER = f"{os.getenv('APP_FOLDER')}/project/static/"

