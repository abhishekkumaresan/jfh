import os
from flask import Flask, send_from_directory
from flask_restful import Api
from flask_cors import CORS  # comment this on deployment
from api import user_api, search_api
from dotenv import load_dotenv
from flask_migrate import Migrate
from api.models import db

from api.config import config
from api.utils import generate_response
from flask_jwt_extended import JWTManager


load_dotenv()

app = Flask(__name__, static_url_path="", static_folder="frontend/build")
app.debug = True
migrate = Migrate(app, db)
CORS(app)  # comment this on deployment
api = Api(app)
jwt = JWTManager(app)

env_config = os.getenv("FLASK_CONFIG", "dev")

app.config.from_object(config[env_config])
db.init_app(app)

with app.app_context():
    db.create_all()


@app.errorhandler(404)
def not_found(e):
    return generate_response(404, "Resource not found.")


@app.errorhandler(400)
def bad_request(e):
    return generate_response(400, "Bad request.")


@app.route("/", defaults={"path": ""})
def serve(path):
    return send_from_directory(app.static_folder, "index.html")


api.add_resource(user_api.UserListAPI, "/api/users")
api.add_resource(user_api.UserAPI, "/api/user/<int:id>")
api.add_resource(user_api.Login, "/api/auth/login")
api.add_resource(user_api.TokenRefresh, "/api/auth/refresh")
api.add_resource(search_api.SearchListAPI, "/api/mysearches")
api.add_resource(search_api.SearchAPI, "/api/search/<string:city>")
