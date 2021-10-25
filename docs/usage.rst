Usage Examples
==============

Flask-PASETO-Extended provides three classes for each purpose.

.. contents::
   :local:

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

PasetoVerifier
--------------

This class can be used for verifying public (signed) PASETO. It is suitable for using PASETO as API tokens.

T.B.D.

.. _`examples/cookie_session.py`: https://github.com/dajiaji/flask-paseto-extended/blob/main/examples/cookie_session.py
.. _`examples/login_manager.py`: https://github.com/dajiaji/flask-paseto-extended/blob/main/examples/login_manager.py
.. _`Flask-Login`: https://github.com/maxcountryman/flask-login
