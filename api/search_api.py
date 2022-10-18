from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity
from api.models import Search
from .validation_models import search_shema
from flask import current_app
import requests
import logging
from datetime import datetime


class SearchAPI(Resource):
    @jwt_required()
    def get(self, city):

        headers = {"Accept-Encoding": "gzip"}
        city_key_response = requests.get(
            f"{current_app.config['ACCU_WEATHER_DOMAIN']}{current_app.config['ACCU_WEATHER_CITY_SEARCH']}?apikey={current_app.config['ACCU_WEATHER_API_KEY']}&q={city}",
            headers=headers,
        )
        try:
            data = city_key_response.json()
            if len(data) > 0:
                key = data[0].get("Key")
                city_wearther_response = requests.get(
                    f"{current_app.config['ACCU_WEATHER_DOMAIN']}{current_app.config['ACCU_WEATHER_LOCATION']}/{key}?apikey={current_app.config['ACCU_WEATHER_API_KEY']}&details=true",
                    headers=headers,
                )
                try:
                    weather_data = city_wearther_response.json()
                    if len(weather_data) == 0:
                        return weather_data
                    weather_data = weather_data[0]
                    search_result = {
                        "user_name": get_jwt_identity(),
                        "search_city": city,
                        "observation_time": datetime.strptime(
                            weather_data.get("LocalObservationDateTime"),
                            "%Y-%m-%dT%H:%M:%S%z",
                        ),
                        "weather": weather_data.get("WeatherText"),
                        "temperature_celicius": weather_data.get("Temperature")
                        .get("Metric")
                        .get("Value"),
                        "temperature_celicius_indoor": weather_data.get(
                            "RealFeelTemperature"
                        )
                        .get("Metric")
                        .get("Value"),
                        "humidity": weather_data.get("RelativeHumidity"),
                        "humidity_indoor": weather_data.get("IndoorRelativeHumidity"),
                    }
                    search_obj = Search(**search_result)
                    search_obj.save_to_db()
                    return search_shema.dump(search_result)

                except Exception as e:
                    logging.info("Exception when getting weather data for key")
                    logging.info(city_wearther_response.text)
                    logging.error(e)

                    return {"messgae": "Something went wrong"}, 500
        except Exception as e:
            logging.info("Exception when getting weather data for key")
            logging.info(city_key_response.text)
            logging.error(e)

            return {"messgae": "Something went wrong"}, 500


class SearchListAPI(Resource):
    @jwt_required()
    def get(self):
        identity = get_jwt_identity()
        return {
            "searches": search_shema.dump(Search.find_by_user_name(identity), many=True)
        }
