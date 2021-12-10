Usage Examples
==============

Flask-PASETO-Extended provides three classes for each purpose.

.. contents::
   :local:

PasetoIssuer
------------

This class can be used for issuing `public` (signed) PASETO. It is suitable for using PASETO as API tokens. By using `PasetoIssuer`, you can easily implement the endpoint issuing PASETO tokens as follows:

.. code-block:: python

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
    # app.config["PASETO_USE_ISS"] = True
    # app.config["PASETO_USE_IAT"] = False
    # app.config["PASETO_EXP"] = 3600  # in seconds
    # app.config["PASETO_USE_KID"] = False
    # app.config["PASETO_SERIALIZER"] = json # or e.g., cbor2
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

See `examples/issuer_and_verifier.py`_ for a sample code that actually works.

PasetoVerifier
--------------

This class can be used for verifying `public` (signed) PASETO. It is suitable for using PASETO as API tokens. By using `PasetoVerifier`, you can easily implement the endpoint verifying PASETO tokens. You can enable PASETO token verification in your APIs by simply adding `@paseto_required` decorator to the API definitions. In the APIs, you can refer to the veified PASETO token with `current_paseto`.

.. code-block:: python

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
    # app.config["PASETO_SKEW"] = 60  # in seconds
    # app.config["PASETO_DESERIALIZER"] = json # or e.g., cbor2
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

See `examples/issuer_and_verifier.py`_ for a sample code that actually works.

PasetoCookieSessionInterface
----------------------------

Flask stores session information as a Cookie value.
By using this class, you can serialize the session information as an encrypted PASETO.

`PasetoCookieSessionInterface` can be used as follows:

.. code-block:: python

    import flask
    from flask_paseto_extended import PasetoCookieSessionInterface

    app = flask.Flask(__name__)
    app.secret_key = "super secret string"

    # Use PASETO("v4" by default) for cookie sessions.
    app.session_interface = PasetoCookieSessionInterface()


See `examples/cookie_session.py`_ for a sample code that actually works.

PasetoLoginManager
------------------

By using this class together with `Flask-Login`_, you can use PASETO for remember-me tokens
which is also encoded into a Cookie value.

`PasetoLoginManager` can be used as follows:

.. code-block:: python

    import flask
    import flask_login

    # Import PasetoLoginManager instead of flask_login.LoginManager.
    from flask_paseto_extended import PasetoLoginManager

    app = flask.Flask(__name__)
    app.secret_key = "super secret string"

    login_manager = PasetoLoginManager(app)

See `examples/login_manager.py`_ for a sample code that actually works.

.. _`examples/issuer_and_verifier.py`: https://github.com/dajiaji/flask-paseto-extended/blob/main/examples/issuer_and_verifier.py
.. _`examples/cookie_session.py`: https://github.com/dajiaji/flask-paseto-extended/blob/main/examples/cookie_session.py
.. _`examples/login_manager.py`: https://github.com/dajiaji/flask-paseto-extended/blob/main/examples/login_manager.py
.. _`Flask-Login`: https://github.com/maxcountryman/flask-login
