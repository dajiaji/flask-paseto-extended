# Flask PASETO Extended

![Flask PASETO Extended](https://github.com/dajiaji/flask-paseto-extended/wiki/images/flask_paseto_extended_header.png)

[![PyPI version](https://badge.fury.io/py/flask-paseto-extended.svg)](https://badge.fury.io/py/flask-paseto-extended)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/flask-paseto-extended)
[![Documentation Status](https://readthedocs.org/projects/flask-paseto-extended/badge/?version=latest)](https://flask-paseto-extended.readthedocs.io/en/latest/?badge=latest)
![Github CI](https://github.com/dajiaji/flask-paseto-extended/actions/workflows/python-package.yml/badge.svg)
[![codecov](https://codecov.io/gh/dajiaji/flask-paseto-extended/branch/main/graph/badge.svg?token=QN8GXEYEP3)](https://codecov.io/gh/dajiaji/flask-paseto-extended)

Flask-PASETO-Extended provides following four classes to use [PASETO (Platform-Agnostic Security Tokens)](https://paseto.io/) for Flask applications:

- **PasetoIssuer**
  - This class can be used for issuing `public` (signed) PASETO. It is suitable for using PASETO as API tokens.
- **PasetoVerifier**
  - This class can be used for verifying `public` (signed) PASETO. It is suitable for using PASETO as API tokens.
- **PasetoCookieSessionInterface**
  - Flask (`Flask.sessions`) stores session information as a Cookie value. By using this class, you can serialize the session information as a `local` (encrypted and then MACed) PASETO.
- **PasetoLoginManager**
  - By using this class together with [Flask-Login](https://github.com/maxcountryman/flask-login), you can use a `local` PASETO for remember-me tokens which is also encoded into a Cookie value.

For encoding/decoding PASETO, we have adopted [PySETO](https://github.com/dajiaji/pyseto),
which is a PASETO/PASERK implementation supporting all of PASETO versions (
[v4](https://github.com/paseto-standard/paseto-spec/blob/master/docs/01-Protocol-Versions/Version4.md),
[v3](https://github.com/paseto-standard/paseto-spec/blob/master/docs/01-Protocol-Versions/Version3.md),
[v2](https://github.com/paseto-standard/paseto-spec/blob/master/docs/01-Protocol-Versions/Version2.md) and
[v1](https://github.com/paseto-standard/paseto-spec/blob/master/docs/01-Protocol-Versions/Version1.md)) and purposes (`local` and `public`).

## Index
- [Installation](#installation)
- [Basic Usage](#basic-usage)
  - [PasetoIssuer/PasetoVerifier](#pasetoissuerverifier)
  - [PasetoCookieSessionInterface](#pasetocookiesessioninterface)
  - [PasetoLoginManager](#pasetologinmanager)
- [API Reference](#api-reference)
- [Tests](#tests)
- [Contributing](#contributing)

## Installation

You can install Flask-PASETO-Extended with pip:

```sh
$ pip install flask-paseto-extended
```

## Basic Usage

Flask-PASETO-Extended provides three classes for each purpose.

### PasetoIssuer/Verifier

`PasetoIssuer` and `PasetoVerifier` can be used for issuing and verifying `public` (signed) PASETO tokens.

By using `PasetoIssuer`, you can easily implement the endpoint issuing PASETO tokens as follows:

```py
import flask

from flask_paseto_extended import PasetoIssuer

# Mock user database.
users = {"foo@bar.example": {"password": "mysecret"}}


app = flask.Flask(__name__)

app.config["PASETO_ISS"] = "https://issuer.example"
app.config["PASETO_PRIVATE_KEYS"] = [
    {
        "version": 4,
        "key": "-----BEGIN PRIVATE KEY-----\nMC4CAQAwBQYDK2VwBCIEILTL+0PfTOIQcn2VPkpxMwf6Gbt9n4UEFDjZ4RuUKjd0\n-----END PRIVATE KEY-----",
    },
    # PASERK can also be used (RECOMMENDED).
    # {
    #     "paserk": "k4.secret.tMv7Q99M4hByfZU-SnEzB_oZu32fhQQUONnhG5QqN3Qeudu7vAR8A_1wYE4AcfCYfhayi3VyJcEfAEFdDiCxog",
    # },
]
issuer = PasetoIssuer(app)


@app.route("/login", methods=["POST"])
def login():
    email = flask.request.form["email"]
    if flask.request.form["password"] != users[email]["password"]:
        return "Bad login"

    token = issuer.issue(payload={"user": {"email": email}})
    resp = flask.redirect(flask.url_for("protected_me"))
    resp.set_cookie(
        "paseto", token, httponly=True
    )  # Note: MUST add secure=True in production
    return resp
```

On the other hand, by using `PasetoVerifier`, you can easily implement the endpoint verifying PASETO tokens. You can enable PASETO token verification in your APIs by simply adding `@paseto_required` decorator to the API definitions. In the APIs, you can refer to the veified PASETO token with `current_paseto`.

```py
import flask
from flask import jsonify, make_response

from flask_paseto_extended import PasetoVerifier, current_paseto, paseto_required

# Mock user database.
users = {"foo@bar.example": {"password": "mysecret"}}

app = flask.Flask(__name__)

# Configurations for PasetoVerifier.
app.config["PASETO_PUBLIC_KEYS"] = [
    {
        "iss": "https://issuer.exmaple",
        "version": 4,
        "key": "-----BEGIN PUBLIC KEY-----\nMCowBQYDK2VwAyEAHrnbu7wEfAP9cGBOAHHwmH4Wsot1ciXBHwBBXQ4gsaI=\n-----END PUBLIC KEY-----",
    },
    # PASERK can also be used (RECOMMENDED).
    # {
    #     "iss": "https://issuer.exmaple",
    #     "paserk": "k4.public.Hrnbu7wEfAP9cGBOAHHwmH4Wsot1ciXBHwBBXQ4gsaI",
    # },
]
verifier = PasetoVerifier(app)


@verifier.token_loader
def token_loader(req: flask.Request):
    # You must implement a callback func to extract a PASETO token from each request.
    return req.cookies.get("paseto", None)


@verifier.verification_error_handler
def verification_error_handler():
    # You must also implement a callback func to handle token verification errors..
    resp = make_response("Unauthorized")
    resp.delete_cookie("paseto", httponly=True)
    return resp


@app.route("/protected/me")
@paseto_required()
def protected_me():
    return jsonify(current_paseto.payload["user"])
```

See [examples/issuer_and_verifier.py](https://github.com/dajiaji/flask-paseto-extended/blob/main/examples/issuer_and_verifier.py) for a sample code that actually works.


### PasetoCookieSessionInterface

Flask (`Flask.sessions`) stores session information as a Cookie value. By using this class, you can serialize the session information as an encrypted (and then MACed) PASETO.

This class can be used as follows:

```py
import flask
from flask_paseto_extended import PasetoCookieSessionInterface

app = flask.Flask(__name__)
app.secret_key = "super secret string"

# Use PASETO("v4" by default) for cookie sessions.
app.session_interface = PasetoCookieSessionInterface()
```

See [examples/cookie_session.py](https://github.com/dajiaji/flask-paseto-extended/blob/main/examples/cookie_session.py) for a sample code that actually works.

### PasetoLoginManager

By using this class together with [Flask-Login](https://github.com/maxcountryman/flask-login), you can use PASETO for remember-me tokens which is also encoded into a Cookie value.

This class can be used as follows:

```py
import flask
import flask_login

# Import PasetoLoginManager instead of flask_login.LoginManager.
from flask_paseto_extended import PasetoLoginManager

app = flask.Flask(__name__)
app.secret_key = "super secret string"

login_manager = PasetoLoginManager(app)
```

See [examples/login_manager.py](https://github.com/dajiaji/flask-paseto-extended/blob/main/examples/login_manager.py) for a sample code that actually works.

## API Reference

See [Documentation](https://flask-paseto-extended.readthedocs.io/en/stable/api.html).


## Tests

You can run tests from the project root after cloning with:

```sh
$ tox
```

## Contributing

We welcome all kind of contributions, filing issues, suggesting new features or sending PRs.
