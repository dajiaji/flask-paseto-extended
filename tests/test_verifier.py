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
def app_with_wrong_public_key():

    users = {"foo@bar.example": {"password": "mysecret"}}

    app = flask.Flask(__name__)

    app.config["PASETO_ISS"] = "https://issuer.example"
    app.config["PASETO_PRIVATE_KEYS"] = [
        {
            "version": 4,
            "key": "-----BEGIN PRIVATE KEY-----\nMC4CAQAwBQYDK2VwBCIEILTL+0PfTOIQcn2VPkpxMwf6Gbt9n4UEFDjZ4RuUKjd0\n-----END PRIVATE KEY-----",
        },
    ]
    issuer = PasetoIssuer(app)

    app.config["PASETO_PUBLIC_KEYS"] = [
        {
            "iss": "https://issuer.exmaple",
            "version": 4,
            # The following public key is not derived from the above private key.
            "key": "-----BEGIN PUBLIC KEY-----\nMCowBQYDK2VwAyEAkv4y3wCgwetRuJUt/EKjNJzaTWMKCNcadaGg6obUFdI=\n-----END PUBLIC KEY-----",
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
        # Token verification always fails.
        return jsonify(current_paseto.payload["user"])

    return app


@pytest.fixture(scope="function")
def app_without_verifier():

    users = {"foo@bar.example": {"password": "mysecret"}}

    app = flask.Flask(__name__)

    app.config["PASETO_ISS"] = "https://issuer.example"
    app.config["PASETO_PRIVATE_KEYS"] = [
        {
            "version": 4,
            "key": "-----BEGIN PRIVATE KEY-----\nMC4CAQAwBQYDK2VwBCIEILTL+0PfTOIQcn2VPkpxMwf6Gbt9n4UEFDjZ4RuUKjd0\n-----END PRIVATE KEY-----",
        },
    ]
    issuer = PasetoIssuer(app)

    # app.config["PASETO_PUBLIC_KEYS"] = [
    #     {
    #         "iss": "https://issuer.exmaple",
    #         "version": 4,
    #         "key": "-----BEGIN PUBLIC KEY-----\nMCowBQYDK2VwAyEAHrnbu7wEfAP9cGBOAHHwmH4Wsot1ciXBHwBBXQ4gsaI=\n-----END PUBLIC KEY-----",
    #     },
    # ]
    # verifier = PasetoVerifier(app)

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
        # Token verification always fails.
        return jsonify(current_paseto.payload["user"])

    return app


class TestPasetoVerifier:
    """
    Tests for PasetoVerifier.
    """

    def test_verifier(self):

        app = flask.Flask(__name__)
        app.config["PASETO_SKEW"] = 60
        app.config["PASETO_PUBLIC_KEYS"] = [
            {
                "iss": "https://issuer.exmaple",
                "version": 4,
                "key": "-----BEGIN PUBLIC KEY-----\nMCowBQYDK2VwAyEAHrnbu7wEfAP9cGBOAHHwmH4Wsot1ciXBHwBBXQ4gsaI=\n-----END PUBLIC KEY-----",
            },
        ]
        verifier = PasetoVerifier(app)
        assert hasattr(verifier, "token_loader")
        assert callable(verifier.token_loader)
        assert callable(verifier.token_loader_callback)
        assert hasattr(verifier, "verification_error_handler")
        assert callable(verifier.verification_error_handler)
        assert callable(verifier.verification_error_handler_callback)
        assert hasattr(verifier, "_load_and_verify")
        assert callable(verifier._load_and_verify)

        with pytest.raises(NotImplementedError) as err:
            verifier.token_loader_callback(None)
            pytest.fail("token_loader_callback() must fail.")
        assert "token_loader must be defined." in str(err.value)

        with pytest.raises(NotImplementedError) as err:
            verifier.verification_error_handler_callback()
            pytest.fail("verification_error_handler_callback() must fail.")
        assert "verification_error_handler must be defined." in str(err.value)

    def test_verifier_init_app(self):

        app = flask.Flask(__name__)
        app.config["PASETO_SKEW"] = 60
        app.config["PASETO_PUBLIC_KEYS"] = [
            {
                "iss": "https://issuer.exmaple",
                "version": 4,
                "key": "-----BEGIN PUBLIC KEY-----\nMCowBQYDK2VwAyEAHrnbu7wEfAP9cGBOAHHwmH4Wsot1ciXBHwBBXQ4gsaI=\n-----END PUBLIC KEY-----",
            },
        ]
        verifier = PasetoVerifier()
        verifier.init_app(app)
        assert hasattr(verifier, "token_loader")
        assert callable(verifier.token_loader)
        assert callable(verifier.token_loader_callback)
        assert hasattr(verifier, "verification_error_handler")
        assert callable(verifier.verification_error_handler)
        assert callable(verifier.verification_error_handler_callback)
        assert hasattr(verifier, "_load_and_verify")
        assert callable(verifier._load_and_verify)

        with pytest.raises(NotImplementedError) as err:
            verifier.token_loader_callback(None)
            pytest.fail("token_loader_callback() must fail.")
        assert "token_loader must be defined." in str(err.value)

        with pytest.raises(NotImplementedError) as err:
            verifier.verification_error_handler_callback()
            pytest.fail("verification_error_handler_callback() must fail.")
        assert "verification_error_handler must be defined." in str(err.value)

    def test_verifier_init_app_with_paserk(self):

        app = flask.Flask(__name__)
        app.config["PASETO_SKEW"] = 60
        app.config["PASETO_PUBLIC_KEYS"] = [
            {
                "iss": "https://issuer.exmaple",
                "paserk": "k4.public.Hrnbu7wEfAP9cGBOAHHwmH4Wsot1ciXBHwBBXQ4gsaI",
            },
        ]
        verifier = PasetoVerifier()
        verifier.init_app(app)
        assert hasattr(verifier, "token_loader")

    def test_verifier_init_app_with_multiple_paserks(self):

        app = flask.Flask(__name__)
        app.config["PASETO_SKEW"] = 60
        app.config["PASETO_PUBLIC_KEYS"] = [
            {
                "paserk": "k4.public.Hrnbu7wEfAP9cGBOAHHwmH4Wsot1ciXBHwBBXQ4gsaI",
            },
            {
                "paserk": "k3.public.AnBxcnN0dXZ3eHl6e3x9fn-AgYKDhIWGh4iJiouMjY6PkJGSk5SVlpeYmZqbnJ2enw",
            },
        ]
        verifier = PasetoVerifier()
        verifier.init_app(app)
        assert hasattr(verifier, "token_loader")

    def test_verifier_paseto_verification_failed(self, app_with_wrong_public_key):

        with app_with_wrong_public_key.test_client() as c:
            res = c.post(
                "/login",
                data=dict(email="foo@bar.example", password="mysecret"),
                follow_redirects=True,
            )
            assert res.status_code == 200
            res = c.get("/protected")
            assert res.status_code == 200
            assert res.data == b"Unauthorized"

    def test_verifier_paseto_required_before_setting(self, app_without_verifier):

        with app_without_verifier.test_client() as c:
            res = c.post(
                "/login",
                data=dict(email="foo@bar.example", password="mysecret"),
                follow_redirects=True,
            )
            assert res.status_code == 500

    @pytest.mark.parametrize(
        "skew, msg",
        [
            (-1, "PASETO_SKEW must be int (>= 0)."),
            (-3600, "PASETO_SKEW must be int (>= 0)."),
            ("3600", "PASETO_SKEW must be int (>= 0)."),
            ([3600], "PASETO_SKEW must be int (>= 0)."),
            ({"value": 3600}, "PASETO_SKEW must be int (>= 0)."),
        ],
    )
    def test_verifier_with_invalid_skew(self, skew, msg):

        app = flask.Flask(__name__)
        app.config["PASETO_SKEW"] = skew
        app.config["PASETO_PUBLIC_KEYS"] = [
            {
                "iss": "https://issuer.exmaple",
                "version": 4,
                "key": "-----BEGIN PUBLIC KEY-----\nMCowBQYDK2VwAyEAHrnbu7wEfAP9cGBOAHHwmH4Wsot1ciXBHwBBXQ4gsaI=\n-----END PUBLIC KEY-----",
            },
        ]
        with pytest.raises(ValueError) as err:
            PasetoVerifier(app)
            pytest.fail("init_app() must fail.")
        assert msg in str(err.value)

    @pytest.mark.parametrize(
        "deserializer, msg",
        [
            (1, "PASETO_DESERIALIZER must have a callable 'loads'."),
            ("string", "PASETO_DESERIALIZER must have a callable 'loads'."),
            ({"loads": ""}, "PASETO_DESERIALIZER must have a callable 'loads'."),
        ],
    )
    def test_verifier_with_invalid_deserializer(self, deserializer, msg):

        app = flask.Flask(__name__)
        app.config["PASETO_SKEW"] = 60
        app.config["PASETO_DESERIALIZER"] = deserializer
        app.config["PASETO_PUBLIC_KEYS"] = [
            {
                "iss": "https://issuer.exmaple",
                "version": 4,
                "key": "-----BEGIN PUBLIC KEY-----\nMCowBQYDK2VwAyEAHrnbu7wEfAP9cGBOAHHwmH4Wsot1ciXBHwBBXQ4gsaI=\n-----END PUBLIC KEY-----",
            },
        ]
        with pytest.raises(ValueError) as err:
            PasetoVerifier(app)
            pytest.fail("init_app() must fail.")
        assert msg in str(err.value)

    @pytest.mark.parametrize(
        "keys, msg",
        [
            ([], "PASETO_PUBLIC_KEYS must be set."),
            (
                [{}],
                "A key object must have a 'paserk' or a pair of 'version' and 'key'.",
            ),
            (
                [{"paserk": "k4.public.xxx"}],
                "Invalid PASERK data.",
            ),
            (
                [{"paserk": "k4.local.b3VyLXNlY3JldA"}],
                "A local key is not allowed.",
            ),
            (
                [{"version": "xxx"}],
                "A 'version' in PASETO_PUBLIC_KEYS must be int.",
            ),
            (
                [{"version": 0}],
                "Invalid PASETO version: 0.",
            ),
            (
                [{"version": 4}],
                "A key object must have a 'paserk' or a pair of 'version' and 'key'.",
            ),
            (
                [{"version": 4, "key": "xxx"}],
                "A 'key' must be a PEM formatted key.",
            ),
            (
                [
                    {
                        "iss": 1,
                        "paserk": "k4.public.Hrnbu7wEfAP9cGBOAHHwmH4Wsot1ciXBHwBBXQ4gsaI",
                    }
                ],
                "An 'iss' must be str.",
            ),
        ],
    )
    def test_verifier_with_invalid_keys(self, keys, msg):

        app = flask.Flask(__name__)
        app.config["PASETO_SKEW"] = 60
        app.config["PASETO_PUBLIC_KEYS"] = keys
        with pytest.raises(ValueError) as err:
            PasetoVerifier(app)
            pytest.fail("init_app() must fail.")
        assert msg in str(err.value)
