# flake8: noqa: E501
import json

import flask
import pyseto
import pytest
from pyseto import Key

from flask_paseto_extended import EncodeError, PasetoIssuer


class TestPasetoIssuer:
    """
    Tests for PasetoIssuer.
    """

    def test_issuer(self):
        app = flask.Flask(__name__)
        app.config["PASETO_ISS"] = "https://issuer.example"
        app.config["PASETO_USE_ISS"] = False
        app.config["PASETO_USE_IAT"] = True
        app.config["PASETO_EXP"] = 3600
        app.config["PASETO_USE_KID"] = True
        app.config["PASETO_SERIALIZER"] = json
        app.config["PASETO_PRIVATE_KEYS"] = [
            {
                "version": 4,
                "key": "-----BEGIN PRIVATE KEY-----\nMC4CAQAwBQYDK2VwBCIEILTL+0PfTOIQcn2VPkpxMwf6Gbt9n4UEFDjZ4RuUKjd0\n-----END PRIVATE KEY-----",
            },
        ]
        issuer = PasetoIssuer(app)
        assert hasattr(issuer, "issue")
        assert callable(issuer.issue)
        token = issuer.issue({"key": "value"})
        assert isinstance(token, bytes)
        key = Key.new(
            4,
            "public",
            "-----BEGIN PUBLIC KEY-----\nMCowBQYDK2VwAyEAHrnbu7wEfAP9cGBOAHHwmH4Wsot1ciXBHwBBXQ4gsaI=\n-----END PUBLIC KEY-----",
        )
        decoded = pyseto.decode(key, token, deserializer=json)
        assert "kid" in decoded.footer

    def test_issuer_with_mandatory_configs(self):
        app = flask.Flask(__name__)
        app.config["PASETO_ISS"] = "https://issuer.example"
        app.config["PASETO_PRIVATE_KEYS"] = [
            {
                "version": 4,
                "key": "-----BEGIN PRIVATE KEY-----\nMC4CAQAwBQYDK2VwBCIEILTL+0PfTOIQcn2VPkpxMwf6Gbt9n4UEFDjZ4RuUKjd0\n-----END PRIVATE KEY-----",
            },
        ]
        issuer = PasetoIssuer(app)
        assert hasattr(issuer, "issue")
        assert callable(issuer.issue)

    def test_issuer_init_app(self):
        app = flask.Flask(__name__)
        app.config["PASETO_ISS"] = "https://issuer.example"
        app.config["PASETO_PRIVATE_KEYS"] = [
            {
                "version": 4,
                "key": "-----BEGIN PRIVATE KEY-----\nMC4CAQAwBQYDK2VwBCIEILTL+0PfTOIQcn2VPkpxMwf6Gbt9n4UEFDjZ4RuUKjd0\n-----END PRIVATE KEY-----",
            },
        ]
        issuer = PasetoIssuer()
        issuer.init_app(app)
        assert hasattr(issuer, "issue")
        assert callable(issuer.issue)

    def test_issuer_with_multiple_keys(self):
        app = flask.Flask(__name__)
        app.config["PASETO_ISS"] = "https://issuer.example"
        app.config["PASETO_PRIVATE_KEYS"] = [
            {
                "version": 4,
                "key": "-----BEGIN PRIVATE KEY-----\nMC4CAQAwBQYDK2VwBCIEILTL+0PfTOIQcn2VPkpxMwf6Gbt9n4UEFDjZ4RuUKjd0\n-----END PRIVATE KEY-----",
            },
            {
                "version": 4,
                "key": "-----BEGIN PRIVATE KEY-----\nMC4CAQAwBQYDK2VwBCIEIGmfHRcqkCfnAOB7234NNeuBpHUVHSLX4z3s4hsaTEQ8\n-----END PRIVATE KEY-----",
            },
        ]
        issuer = PasetoIssuer(app)
        assert hasattr(issuer, "issue")
        assert callable(issuer.issue)

    def test_issuer_init_app_with_paserk(self):
        app = flask.Flask(__name__)
        app.config["PASETO_ISS"] = "https://issuer.example"
        app.config["PASETO_PRIVATE_KEYS"] = [
            {
                "iss": "https://issuer.exmaple",
                "paserk": "k4.secret.cHFyc3R1dnd4eXp7fH1-f4CBgoOEhYaHiImKi4yNjo8c5WpIyC_5kWKhS8VEYSZ05dYfuTF-ZdQFV4D9vLTcNQ",
            },
        ]
        issuer = PasetoIssuer()
        issuer.init_app(app)
        assert hasattr(issuer, "issue")

    def test_issuer_init_app_with_multiple_paserks(self):
        app = flask.Flask(__name__)
        app.config["PASETO_ISS"] = "https://issuer.example"
        app.config["PASETO_PRIVATE_KEYS"] = [
            {
                "paserk": "k4.secret.cHFyc3R1dnd4eXp7fH1-f4CBgoOEhYaHiImKi4yNjo8c5WpIyC_5kWKhS8VEYSZ05dYfuTF-ZdQFV4D9vLTcNQ",
            },
            {
                "paserk": "k3.secret.cHFyc3R1dnd4eXp7fH1-f4CBgoOEhYaHiImKi4yNjo-QkZKTlJWWl5iZmpucnZ6f",
            },
        ]
        issuer = PasetoIssuer()
        issuer.init_app(app)
        assert hasattr(issuer, "issue")

    @pytest.mark.parametrize(
        "iss, msg",
        [
            (None, "PASETO_ISS must be set."),
            ("", "PASETO_ISS must be set."),
            (0, "PASETO_ISS must be set."),
            (1, "PASETO_ISS must be str."),
            (["https://issuer.example"], "PASETO_ISS must be str."),
            ({"iss": "https://issuer.example"}, "PASETO_ISS must be str."),
        ],
    )
    def test_issuer_with_invalid_iss(self, iss, msg):
        app = flask.Flask(__name__)
        app.config["PASETO_ISS"] = iss
        app.config["PASETO_PRIVATE_KEYS"] = [
            {
                "iss": "https://issuer.exmaple",
                "version": 4,
                "key": "-----BEGIN PRIVATE KEY-----\nMC4CAQAwBQYDK2VwBCIEILTL+0PfTOIQcn2VPkpxMwf6Gbt9n4UEFDjZ4RuUKjd0\n-----END PRIVATE KEY-----",
            },
        ]
        with pytest.raises(ValueError) as err:
            PasetoIssuer(app)
            pytest.fail("init_app() must fail.")
        assert msg in str(err.value)

    @pytest.mark.parametrize(
        "use_iss, msg",
        [
            (None, "PASETO_USE_ISS must be bool."),
            ("", "PASETO_USE_ISS must be bool."),
            (b"True", "PASETO_USE_ISS must be bool."),
            ("True", "PASETO_USE_ISS must be bool."),
            (b"False", "PASETO_USE_ISS must be bool."),
            ("False", "PASETO_USE_ISS must be bool."),
            ([True], "PASETO_USE_ISS must be bool."),
            ({"value": True}, "PASETO_USE_ISS must be bool."),
            (100, "PASETO_USE_ISS must be bool."),
        ],
    )
    def test_issuer_with_invalid_use_iss(self, use_iss, msg):
        app = flask.Flask(__name__)
        app.config["PASETO_ISS"] = "https://issuer.example"
        app.config["PASETO_USE_ISS"] = use_iss
        app.config["PASETO_PRIVATE_KEYS"] = [
            {
                "iss": "https://issuer.exmaple",
                "version": 4,
                "key": "-----BEGIN PRIVATE KEY-----\nMC4CAQAwBQYDK2VwBCIEILTL+0PfTOIQcn2VPkpxMwf6Gbt9n4UEFDjZ4RuUKjd0\n-----END PRIVATE KEY-----",
            },
        ]
        with pytest.raises(ValueError) as err:
            PasetoIssuer(app)
            pytest.fail("init_app() must fail.")
        assert msg in str(err.value)

    @pytest.mark.parametrize(
        "use_iat, msg",
        [
            (None, "PASETO_USE_IAT must be bool."),
            ("", "PASETO_USE_IAT must be bool."),
            (b"True", "PASETO_USE_IAT must be bool."),
            ("True", "PASETO_USE_IAT must be bool."),
            (b"False", "PASETO_USE_IAT must be bool."),
            ("False", "PASETO_USE_IAT must be bool."),
            ([True], "PASETO_USE_IAT must be bool."),
            ({"value": True}, "PASETO_USE_IAT must be bool."),
            (100, "PASETO_USE_IAT must be bool."),
        ],
    )
    def test_issuer_with_invalid_use_iat(self, use_iat, msg):
        app = flask.Flask(__name__)
        app.config["PASETO_ISS"] = "https://issuer.example"
        app.config["PASETO_USE_IAT"] = use_iat
        app.config["PASETO_PRIVATE_KEYS"] = [
            {
                "iss": "https://issuer.exmaple",
                "version": 4,
                "key": "-----BEGIN PRIVATE KEY-----\nMC4CAQAwBQYDK2VwBCIEILTL+0PfTOIQcn2VPkpxMwf6Gbt9n4UEFDjZ4RuUKjd0\n-----END PRIVATE KEY-----",
            },
        ]
        with pytest.raises(ValueError) as err:
            PasetoIssuer(app)
            pytest.fail("init_app() must fail.")
        assert msg in str(err.value)

    @pytest.mark.parametrize(
        "exp, msg",
        [
            (-1, "PASETO_EXP must be int (>= 0)."),
            (-3600, "PASETO_EXP must be int (>= 0)."),
            ("3600", "PASETO_EXP must be int (>= 0)."),
            ([3600], "PASETO_EXP must be int (>= 0)."),
            ({"value": 3600}, "PASETO_EXP must be int (>= 0)."),
        ],
    )
    def test_issuer_with_invalid_exp(self, exp, msg):
        app = flask.Flask(__name__)
        app.config["PASETO_ISS"] = "https://issuer.example"
        app.config["PASETO_EXP"] = exp
        app.config["PASETO_PRIVATE_KEYS"] = [
            {
                "iss": "https://issuer.exmaple",
                "version": 4,
                "key": "-----BEGIN PRIVATE KEY-----\nMC4CAQAwBQYDK2VwBCIEILTL+0PfTOIQcn2VPkpxMwf6Gbt9n4UEFDjZ4RuUKjd0\n-----END PRIVATE KEY-----",
            },
        ]
        with pytest.raises(ValueError) as err:
            PasetoIssuer(app)
            pytest.fail("init_app() must fail.")
        assert msg in str(err.value)

    @pytest.mark.parametrize(
        "use_kid, msg",
        [
            (None, "PASETO_USE_KID must be bool."),
            ("", "PASETO_USE_KID must be bool."),
            (b"True", "PASETO_USE_KID must be bool."),
            ("True", "PASETO_USE_KID must be bool."),
            (b"False", "PASETO_USE_KID must be bool."),
            ("False", "PASETO_USE_KID must be bool."),
            ([True], "PASETO_USE_KID must be bool."),
            ({"value": True}, "PASETO_USE_KID must be bool."),
            (100, "PASETO_USE_KID must be bool."),
        ],
    )
    def test_issuer_with_invalid_use_kid(self, use_kid, msg):
        app = flask.Flask(__name__)
        app.config["PASETO_ISS"] = "https://issuer.example"
        app.config["PASETO_USE_KID"] = use_kid
        app.config["PASETO_PRIVATE_KEYS"] = [
            {
                "iss": "https://issuer.exmaple",
                "version": 4,
                "key": "-----BEGIN PRIVATE KEY-----\nMC4CAQAwBQYDK2VwBCIEILTL+0PfTOIQcn2VPkpxMwf6Gbt9n4UEFDjZ4RuUKjd0\n-----END PRIVATE KEY-----",
            },
        ]
        with pytest.raises(ValueError) as err:
            PasetoIssuer(app)
            pytest.fail("init_app() must fail.")
        assert msg in str(err.value)

    @pytest.mark.parametrize(
        "serializer, msg",
        [
            (1, "PASETO_SERIALIZER must have a callable 'dumps'."),
            ("string", "PASETO_SERIALIZER must have a callable 'dumps'."),
            ({"dumps": ""}, "PASETO_SERIALIZER must have a callable 'dumps'."),
        ],
    )
    def test_issuer_with_invalid_serializer(self, serializer, msg):
        app = flask.Flask(__name__)
        app.config["PASETO_ISS"] = "https://issuer.example"
        app.config["PASETO_SERIALIZER"] = serializer
        app.config["PASETO_PRIVATE_KEYS"] = [
            {
                "iss": "https://issuer.exmaple",
                "version": 4,
                "key": "-----BEGIN PRIVATE KEY-----\nMC4CAQAwBQYDK2VwBCIEILTL+0PfTOIQcn2VPkpxMwf6Gbt9n4UEFDjZ4RuUKjd0\n-----END PRIVATE KEY-----",
            },
        ]
        with pytest.raises(ValueError) as err:
            PasetoIssuer(app)
            pytest.fail("init_app() must fail.")
        assert msg in str(err.value)

    @pytest.mark.parametrize(
        "keys, msg",
        [
            ([], "PASETO_PRIVATE_KEYS must be set."),
            (
                [{}],
                "A key object must have a 'paserk' or a pair of 'version' and 'key'.",
            ),
            (
                [{"paserk": "k4.secret.xxx"}],
                "Invalid PASERK data.",
            ),
            (
                [{"paserk": "k4.local.b3VyLXNlY3JldA"}],
                "A local key is not allowed.",
            ),
            (
                [{"version": "xxx"}],
                "A 'version' in PASETO_PRIVATE_KEYS must be int.",
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
        ],
    )
    def test_issuer_with_invalid_keys(self, keys, msg):
        app = flask.Flask(__name__)
        app.config["PASETO_ISS"] = "https://issuer.example"
        app.config["PASETO_PRIVATE_KEYS"] = keys
        with pytest.raises(ValueError) as err:
            PasetoIssuer(app)
            pytest.fail("init_app() must fail.")
        assert msg in str(err.value)

    def test_issuer_issue_with_bad_kid(self):
        app = flask.Flask(__name__)
        app.config["PASETO_ISS"] = "https://issuer.example"
        app.config["PASETO_PRIVATE_KEYS"] = [
            {
                "version": 4,
                "key": "-----BEGIN PRIVATE KEY-----\nMC4CAQAwBQYDK2VwBCIEILTL+0PfTOIQcn2VPkpxMwf6Gbt9n4UEFDjZ4RuUKjd0\n-----END PRIVATE KEY-----",
            },
            {
                "version": 4,
                "key": "-----BEGIN PRIVATE KEY-----\nMC4CAQAwBQYDK2VwBCIEIGmfHRcqkCfnAOB7234NNeuBpHUVHSLX4z3s4hsaTEQ8\n-----END PRIVATE KEY-----",
            },
        ]
        issuer = PasetoIssuer(app)
        with pytest.raises(ValueError) as err:
            issuer.issue(
                {"foo": "bar"},
                kid="k3.pid.gnwg7IkzZyQF9wJgLLT0OpbdMT7BYmdQoG2u-xXpeeHz",
            )
            pytest.fail("issue() must fail.")
        assert "A signing key is not found." in str(err.value)

    def test_issuer_issue_with_bad_serializer(self):
        class _BadSerializer:
            def dumps(*args, **kwargs):
                raise NotImplementedError("Not implemented.")

        app = flask.Flask(__name__)
        app.config["PASETO_ISS"] = "https://issuer.example"
        app.config["PASETO_SERIALIZER"] = _BadSerializer()
        app.config["PASETO_PRIVATE_KEYS"] = [
            {
                "version": 4,
                "key": "-----BEGIN PRIVATE KEY-----\nMC4CAQAwBQYDK2VwBCIEILTL+0PfTOIQcn2VPkpxMwf6Gbt9n4UEFDjZ4RuUKjd0\n-----END PRIVATE KEY-----",
            },
        ]
        issuer = PasetoIssuer(app)
        with pytest.raises(EncodeError) as err:
            issuer.issue({"foo": "bar"})
            pytest.fail("issue() must fail.")
        assert "Failed to encode a token." in str(err.value)
