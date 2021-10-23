from secrets import token_bytes

import flask
import flask_login
import pytest
from flask_login import LoginManager

from flask_paseto_extended import PasetoCookieSessionInterface


class InvalidCookieClient(object):
    def __init__(self, app):

        self.app = app

    def __call__(self, environ, start_response):

        invalid_session = "v4.local.WQ8aDTTIbGL9FmTsdBeYoFTciDXl25i5xCbX6W-vpZ342mFyEOg08ghnSGIKqg2lMUGUDvgYly_o0QtGtSCpAl0IFgwLWvrkn9TI_Qfyv1SUbTOCGdPDNxDFlY8JALm9yO_MddM7dCUgrM4M6ofbNh6HiDqhmNr64wbjcdoYTLhsZxgRBVoOwTbtAYWaO-gp7msnGsr2zrJjZcJKEvPcLacHLh3tTWxJoHt41KRThTHlkicf9KHCWJXNA4jM7gWiDBiHdZjMC2_JsUyPDRhnMD1jNbQkakJY0tEAaiXWq9To_fa4BUgDYl4unIl5WQ08ZMa2560"

        environ["HTTP_COOKIE"] = environ.get(
            "HTTP_COOKIE", f"session={invalid_session}"
        )
        return self.app(environ, start_response)


@pytest.fixture(scope="function")
def app():

    app = flask.Flask(__name__)

    login_manager = LoginManager(app)

    # Our mock database.
    users = {"foo@bar.example": {"password": "mysecret"}}

    # Our simple user class
    class User(flask_login.UserMixin):
        pass

    @login_manager.user_loader
    def user_loader(email):

        if email not in users:
            return

        user = User()
        user.id = email
        return user

    @login_manager.request_loader
    def request_loader(request):

        email = request.form.get("email")
        if email not in users:
            return

        user = User()
        user.id = email
        return user

    @login_manager.unauthorized_handler
    def unauthorized_handler():
        return "Unauthorized"

    @app.route("/login", methods=["POST"])
    def login():

        email = flask.request.form["email"]
        if flask.request.form["password"] == users[email]["password"]:
            user = User()
            user.id = email
            flask_login.login_user(user)
            return flask.redirect(flask.url_for("protected"))
        return "Bad login"

    @app.route("/logout")
    def logout():

        flask_login.logout_user()
        return "Logged out"

    @app.route("/protected")
    @flask_login.login_required
    def protected():

        return "Logged in as: " + flask_login.current_user.id

    return app


class TestPasetoCookieSessionInterface:
    """
    Tests for sample code.
    """

    def test_cookie_session(self, app):

        app.secret_key = "super secret string"
        app.session_interface = PasetoCookieSessionInterface()
        with app.test_client() as c:
            res = c.post(
                "/login",
                data=dict(email="foo@bar.example", password="mysecret"),
                follow_redirects=True,
            )
            assert res.status_code == 200
            res = c.get("/protected")
            assert res.status_code == 200
            assert res.data == b"Logged in as: foo@bar.example"
            res = c.get("/logout", follow_redirects=True)
            assert res.status_code == 200

    @pytest.mark.parametrize(
        "version, key",
        [
            (1, "super secret string"),
            (2, token_bytes(32)),
            (3, "super secret string"),
            (4, "super secret string"),
        ],
    )
    def test_cookie_session_with_paseto_version(self, app, version, key):

        app.secret_key = key
        app.session_interface = PasetoCookieSessionInterface(paseto_version=version)
        with app.test_client() as c:
            res = c.post(
                "/login",
                data=dict(email="foo@bar.example", password="mysecret"),
                follow_redirects=True,
            )
            assert res.status_code == 200
            res = c.get("/protected")
            assert res.status_code == 200
            assert res.data == b"Logged in as: foo@bar.example"
            res = c.get("/logout", follow_redirects=True)
            assert res.status_code == 200
            assert res.status_code == 200

    def test_cookie_session_without_secret_key(self, app):

        # app.secret_key = "super secret string"
        app.session_interface = PasetoCookieSessionInterface()
        with app.test_client() as c:
            res = c.post(
                "/login",
                data=dict(email="foo@bar.example", password="mysecret"),
                follow_redirects=True,
            )
            assert res.status_code == 500

    def test_cookie_session_encode_with_invalid_key(self, app):

        app.secret_key = "not 32bytes secret for v2"
        app.session_interface = PasetoCookieSessionInterface(paseto_version=2)
        with app.test_client() as c:
            res = c.post(
                "/login",
                data=dict(email="foo@bar.example", password="mysecret"),
                follow_redirects=True,
            )
            assert res.status_code == 500

    def test_cookie_session_decode_with_another_key(self, app):

        app.secret_key = "super secret string"
        app.session_interface = PasetoCookieSessionInterface()
        with app.test_client() as c:
            res = c.post(
                "/login",
                data=dict(email="foo@bar.example", password="mysecret"),
                follow_redirects=True,
            )
            assert res.status_code == 200

        app.secret_key = "another super secret string"
        with app.test_client() as c:
            res = c.get("/protected")
            assert res.status_code == 200
            assert res.data == b"Unauthorized"

    def test_cookie_session_decode_with_invalid_paseto(self, app):

        app.secret_key = "my super secret"
        app.session_interface = PasetoCookieSessionInterface()
        with app.test_client() as c:
            res = c.post(
                "/login",
                data=dict(email="foo@bar.example", password="mysecret"),
                follow_redirects=True,
            )
            assert res.status_code == 200

        app.wsgi_app = InvalidCookieClient(app.wsgi_app)
        with app.test_client() as c:
            res = c.get("/protected")
            assert res.status_code == 200
            assert res.data == b"Unauthorized"

    @pytest.mark.parametrize(
        "version, msg",
        [
            (0, "Invalid PASETO version: 0"),
            (5, "Invalid PASETO version: 5"),
            (100, "Invalid PASETO version: 100"),
            ("xxx", "Invalid PASETO version: xxx"),
            ({}, "Invalid PASETO version: {}"),
            ([], "Invalid PASETO version: []"),
        ],
    )
    def test_cookie_session_with_invalid_version(self, app, version, msg):

        app.secret_key = "super secret string"
        with pytest.raises(ValueError) as err:
            app.session_interface = PasetoCookieSessionInterface(paseto_version=version)
            pytest.fail("PasetoCookieSessionInterface() should fail.")
        assert msg in str(err.value)
