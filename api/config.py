from datetime import datetime
import os
from datetime import timedelta

db_user = os.environ.get('DB_USER_NAME')
db_password = os.environ.get('DB_PASSWORD')
db_server = os.environ.get('DB_SERVER')
db_name = os.environ.get('DB_NAME')
secret_key = os.environ.get('SECRET_KEY','\xb2\xae\x00\x87\x00\xde\x16L\xa1PD\\\xe7\xcf\x8b\x11')






class BaseConfig:
    DEBUG = False
    JWT_SECRET_KEY = secret_key
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = f'mysql://{db_user}:{db_password}@{db_server}/{db_name}'
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=30)
    ACCU_WEATHER_DOMAIN= os.environ.get("ACCU_WEATHER_DOMAIN","https://dataservice.accuweather.com")
    ACCU_WEATHER_CITY_SEARCH=os.environ.get("ACCU_WEATHER_CITY_SEARCH","/locations/v1/cities/search")
    ACCU_WEATHER_LOCATION=os.environ.get("ACCU_WEATHER_LOCATION","/currentconditions/v1")
    ACCU_WEATHER_API_KEY= os.environ.get("API_KEY")


class DevelopmentConfig(BaseConfig):
    basedir = os.path.abspath(os.path.dirname(__file__))
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = f'mysql://{db_user}:{db_password}@{db_server}/{db_name}'


class ProductionConfig(BaseConfig):
    basedir = os.path.abspath(os.path.dirname(__file__))
    SQLALCHEMY_DATABASE_URI = f'mysql://{db_user}:{db_password}@{db_server}/{db_name}'


config = {
    'dev': 'api.config.DevelopmentConfig',
    'prod': 'api.config.ProductionConfig'
}