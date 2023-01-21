import pickle
import secrets

from flask import Flask, current_app
from flask import make_response, jsonify, request, redirect

from redis.client import Redis

from .tonapi import Tonapi
from .tonapi.exceptions import TonapiError


def index():
    return "Hello, World!"


def add_token(username: str):
    if username:
        if username[-3:].lower() != "bot":
            return jsonify({"error": "Bot username must end with `bot`"}), 400

        auth_token = request.args.get("authToken", None)

        if not auth_token:
            return jsonify({"error": "No authToken provided"}), 400

        tonapi: Tonapi = current_app.config.get("tonapi")
        redis: Redis = current_app.config.get("redis")
        secret_key = secrets.token_hex(32)

        try:
            auth_token = tonapi.get_token(auth_token)

            if auth_token:
                secret_value = pickle.dumps(auth_token.to_dict())

                with redis.client() as client:
                    client.set(secret_key, secret_value, ex=300)

        except TonapiError as error:
            return jsonify({"error": error}), 400

        return redirect(f"https://{username}.t.me?start={secret_key}")

    return jsonify({"error": "No bot username provided"}), 400


def get_auth_token():
    secret_key = request.args.get("secret_key")

    if secret_key:
        redis: Redis = current_app.config.get("redis")

        with redis.client() as client:
            auth_token = client.get(secret_key)

        if auth_token:
            return jsonify(pickle.loads(auth_token))

        return jsonify({"error": "Secret key expired or invalid"}), 400

    return jsonify({"error": "No secret key provided"}), 400


def not_found(_):
    return make_response(jsonify({'error': 'Not found'}), 404)


def register(app: Flask):
    app.register_error_handler(404, not_found)

    app.add_url_rule("/", methods=["GET"], view_func=index)
    app.add_url_rule("/api/getAuthToken", methods=["GET"], view_func=get_auth_token)
    app.add_url_rule("/api/login/bot=<username>", methods=["GET"], view_func=add_token)
