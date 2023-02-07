# flake8: noqa: E501
import json

import flask
import pytest
from flask import jsonify, make_response

from flask_paseto_extended import (
    PasetoIssuer,
    PasetoVerifier,
    current_paseto,
    paseto_required,
)


@pytest.fixture(scope="function")
def app():
    # Mock user database.
    users = {"foo@bar.example": {"password": "mysecret"}}

    app = flask.Flask(__name__)

    # Configurations for PasetoIssuer.
    app.config["PASETO_ISS"] = "https://issuer.example"
    app.config["PASETO_USE_ISS"] = True
    app.config["PASETO_USE_IAT"] = True
    app.config["PASETO_EXP"] = 3600
    app.config["PASETO_PRIVATE_KEYS"] = [
        {
            "version": 4,
            "key": "-----BEGIN PRIVATE KEY-----\nMC4CAQAwBQYDK2VwBCIEILTL+0PfTOIQcn2VPkpxMwf6Gbt9n4UEFDjZ4RuUKjd0\n-----END PRIVATE KEY-----",
        },
    ]
    issuer = PasetoIssuer(app)

    # Configurations for PasetoVerifier.
    app.config["PASETO_SKEW"] = 60  # sec
    app.config["PASETO_PUBLIC_KEYS"] = [
        {
            "iss": "https://issuer.exmaple",
            "version": 4,
            "key": "-----BEGIN PUBLIC KEY-----\nMCowBQYDK2VwAyEAHrnbu7wEfAP9cGBOAHHwmH4Wsot1ciXBHwBBXQ4gsaI=\n-----END PUBLIC KEY-----",
        },
    ]
    verifier = PasetoVerifier(app)

    @verifier.token_loader
    def token_loader(request):
        return request.cookies.get("paseto", None)

    @verifier.verification_error_handler
    def verification_error_handler():
        resp = make_response("Unauthorized")
        resp.delete_cookie("paseto", httponly=True)
        return resp

    @app.route("/login", methods=["GET", "POST"])
    def login():
        email = flask.request.form["email"]
        if flask.request.form["password"] != users[email]["password"]:
            return "Bad login"

        token = issuer.issue(payload={"user": {"email": email}})
        resp = flask.redirect(flask.url_for("protected"))
        resp.set_cookie("paseto", token, httponly=True)
        return resp

    @app.route("/logout")
    def logout():
        resp = make_response("Logged out")
        resp.delete_cookie("paseto", httponly=True)
        return resp

    @app.route("/protected")
    @paseto_required()
    def protected():
        assert current_paseto.is_verified is True
        assert current_paseto.version == "v4"
        assert current_paseto.purpose == "public"
        assert current_paseto.header == b"v4.public."
        assert current_paseto.footer == b""
        assert current_paseto.error is None
        return jsonify(current_paseto.payload["user"])

    return app


class TestPasetoIssuerAndVerifier:
    """
    Tests for sample code (examples/issuer_and_verifier.py).
    """

    def test_issuer_and_verifier(self, app):
        with app.test_client() as c:
            res = c.post(
                "/login",
                data=dict(email="foo@bar.example", password="mysecret"),
                follow_redirects=True,
            )
            assert res.status_code == 200
            res = c.get("/protected")
            assert res.status_code == 200
            body = json.loads(res.data)
            assert body["email"] == "foo@bar.example"
            res = c.get("/logout", follow_redirects=True)
            assert res.status_code == 200

    def test_issuer_and_verifier_without_login(self, app):
        with app.test_client() as c:
            res = c.get("/protected")
            assert res.status_code == 200
            assert res.data == b"Unauthorized"
