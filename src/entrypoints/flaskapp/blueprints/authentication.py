import os
import datetime as dt
from flask import views
from flask_smorest import Blueprint
from marshmallow import Schema, fields
from flask_jwt_extended import create_access_token
from passlib.hash import bcrypt


login = Blueprint(
    "login",
    "login",
    url_prefix="/login",
    description="Authenticate user and issue JWT access tokens",
)


class Credentials(Schema):
    username = fields.String(required=True)
    password = fields.String(required=True)


@login.route("")
class LoginResource(views.MethodView):

    @login.arguments(Credentials)
    @login.response(200)
    def post(self, credentials):

        if credentials["username"] == os.environ["WEB_USERNAME"] and bcrypt.verify(
            credentials["password"], os.environ["WEB_PASSWORD_HASH"]
        ):
            token = create_access_token(
                identity=credentials["username"],
                expires_delta=dt.timedelta(minutes=5),
            )
            return {"access_token": token}

        return {"message": "Invalid credentials"}, 401
