"""Configuration of app"""
import os


basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    """Config for db, static folder, restplus"""
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "postgresql://")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    STATIC_FOLDER = f"{os.getenv('APP_FOLDER')}/project/static/"
    RESTPLUS_VALIDATE = True
    RESTPLUS_MASK_SWAGGER = False
    RESTPLUS_ERROR_404_HELP = False
    RESTPLUS_SWAGGER_UI_DOC_EXPANSION = "list"
