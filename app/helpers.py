from flask import Flask, request, jsonify, make_response, render_template
from flask_sqlalchemy import SQLAlchemy
from functools import wraps

import jwt
import datetime
import re
import os

from werkzeug.security import check_password_hash
import jwt


def verify_user(user, data):

    valid_email = '^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$'

    if user:
        return jsonify({"message":"Email has already been registered"}), 400

    if type(data["name"]) == int:

        return jsonify({"message":"name cannot be an integer"}), 400

    if data['name'] == "" or data['email'] == "" or data['password'] == "":

        return jsonify({"message":"Empty field detected please fill all fields"}), 400

    if data['name'].split() == [] or data['email'].split() == [] or data['password'].split() == []:

        return jsonify({"message":"name/email/password fields cannot be empty"}), 400

    if not re.match(valid_email, data["email"]):

        return jsonify({"message":"Enter a valid email address"}), 400

    if len(data['password'].split()[0]) < 4:

        return jsonify({"message":"password should be at least 4 characters"}), 400
    else:
        return True


def check_fields(data):
    if "name" not in data or "email" not in data or "password" not in data:
        return jsonify({"message":"All fields are required"}), 400
    else:
        return True

def generate_token(user):
    payload = {
        'public_id' : user.public_id,
        'exp' : datetime.datetime.utcnow() + datetime.timedelta(minutes=30)
    }
    secret = os.getenv('SECRET_KEY')
    return jwt.encode(payload, secret)

def check_login(auth):
    if not auth or auth['email'] == "" or auth['password'] == "":
        return jsonify({"message":"Invalid email/password"}), 401
    else:
        return True

def check_user(user, auth):
    if not user:
        return jsonify({"message":"Email has not been registered"}), 401

    if check_password_hash(user.password, auth['password']) != True:
        return jsonify({"message":"Incorrect password"}), 401

    else:
        return True

def check_user_pass(user, reset):
    if not user:
        return jsonify({"message":"email address could not be found"}), 401

    if not check_password_hash(user.password, reset['oldPassword']):
        return jsonify({"message":"old-password is invalid"}), 401

def verify_fields(reset):
    if "email" not in reset or "oldPassword" not in reset or "newPassword" not in reset:
        return jsonify({"message":"All fields are required"}), 400
