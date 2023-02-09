from datetime import timedelta
from secrets import token_bytes

import flask
import flask_login
import pytest
from werkzeug.http import parse_cookie

from flask_paseto_extended import PasetoLoginManager

# Mock database.
users = {"foo@bar.example": {"password": "mysecret"}}


# Simple user class.
class User(flask_login.UserMixin):
    pass


# Wrapper func of PasetoLoginManager().
def new_login_manager(app):
    login_manager = PasetoLoginManager(app)

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

    return login_manager


@pytest.fixture(scope="function")
def app():
    app = flask.Flask(__name__)

    @app.route("/login", methods=["POST"])
    def login():
        email = flask.request.form["email"]
        if flask.request.form["password"] == users[email]["password"]:
            user = User()
            user.id = email
            flask_login.login_user(user, remember=True)
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


@pytest.fixture(scope="function")
def app_with_duration():
    app = flask.Flask(__name__)

    @app.route("/login", methods=["POST"])
    def login():
        email = flask.request.form["email"]
        if flask.request.form["password"] == users[email]["password"]:
            user = User()
            user.id = email
            flask_login.login_user(user, remember=True, duration=timedelta(seconds=1))
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


class TestPasetoLoginManager:
    """
    Tests for PasetoLoginManager.
    """

    def test_login_manager(self, app):
        app.secret_key = "super secret string"
        login_manager = new_login_manager(app)

        assert login_manager.paseto_version == 4

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

    def test_login_manager_with_duration1(self, app):
        app.config["REMEMBER_COOKIE_DURATION"] = 1
        app.secret_key = "super secret string"
        new_login_manager(app)

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

    def test_login_manager_with_duration2(self, app_with_duration):
        # app.config["REMEMBER_COOKIE_DURATION"] = 1
        app_with_duration.secret_key = "super secret string"
        new_login_manager(app_with_duration)

        with app_with_duration.test_client() as c:
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

    def test_login_manager_with_invalid_duration(self, app):
        app.config["REMEMBER_COOKIE_DURATION"] = "1"
        app.secret_key = "super secret string"
        new_login_manager(app)

        with app.test_client() as c:
            res = c.post(
                "/login",
                data=dict(email="foo@bar.example", password="mysecret"),
                follow_redirects=True,
            )
            assert res.status_code == 500

    def test_login_manager_with_refresh(self, app):
        app.config["REMEMBER_COOKIE_DURATION"] = 1
        app.secret_key = "super secret string"
        new_login_manager(app)

        with app.test_client() as c:
            res = c.post(
                "/login",
                data=dict(email="foo@bar.example", password="mysecret"),
                # follow_redirects=True,
            )
            assert res.status_code == 302
            cookie = res.headers.getlist("Set-Cookie")[0]
            remember_token = parse_cookie(cookie)["remember_token"]

        class client(object):
            def __init__(self, app):
                self.app = app

            def __call__(self, environ, start_response):
                environ["HTTP_COOKIE"] = environ.get("HTTP_COOKIE", f"remember_token={remember_token}")
                return self.app(environ, start_response)

        app.wsgi_app = client(app.wsgi_app)
        with app.test_client() as c:
            res = c.get("/protected")
            assert res.status_code == 200
            assert res.data == b"Logged in as: foo@bar.example"

    @pytest.mark.parametrize(
        "version, key",
        [
            (1, "super secret string"),
            (2, token_bytes(32)),
            (3, "super secret string"),
            (4, "super secret string"),
        ],
    )
    def test_login_manager_with_paseto_version(self, app, version, key):
        app.secret_key = key
        app.config["REMEMBER_COOKIE_PASETO_VERSION"] = version

        login_manager = new_login_manager(app)

        assert login_manager.paseto_version == version
        assert login_manager._remember_cookie_key is None

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

    def test_login_manager_with_remember_cookie_key(self, app):
        app.secret_key = "super secret string"
        app.config["REMEMBER_COOKIE_PASETO_KEY"] = "my super secret"
        login_manager = new_login_manager(app)

        assert login_manager.paseto_version == 4

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
        "version, msg",
        [
            (0, "REMEMBER_COOKIE_PASETO_VERSION must be 1, 2, 3 or 4"),
            (5, "REMEMBER_COOKIE_PASETO_VERSION must be 1, 2, 3 or 4"),
            (100, "REMEMBER_COOKIE_PASETO_VERSION must be 1, 2, 3 or 4"),
        ],
    )
    def test_login_manager_with_unsupported_version(self, app, version, msg):
        app.secret_key = "super secret string"
        app.config["REMEMBER_COOKIE_PASETO_VERSION"] = version

        with pytest.raises(ValueError) as err:
            PasetoLoginManager(app)
            pytest.fail("PasetoLoginManager() should fail.")
        assert msg in str(err.value)

    @pytest.mark.parametrize(
        "version, msg",
        [
            ("xxx", "REMEMBER_COOKIE_PASETO_VERSION must be int"),
            ({}, "REMEMBER_COOKIE_PASETO_VERSION must be int"),
            ([], "REMEMBER_COOKIE_PASETO_VERSION must be int"),
        ],
    )
    def test_login_manager_with_invalid_version(self, app, version, msg):
        app.secret_key = "super secret string"
        app.config["REMEMBER_COOKIE_PASETO_VERSION"] = version

        with pytest.raises(TypeError) as err:
            PasetoLoginManager(app)
            pytest.fail("PasetoLoginManager() should fail.")
        assert msg in str(err.value)

    @pytest.mark.parametrize(
        "key, msg",
        [
            (12345, "REMEMBER_COOKIE_PASETO_KEY must be str"),
            (b"my secret", "REMEMBER_COOKIE_PASETO_KEY must be str"),
            ({}, "REMEMBER_COOKIE_PASETO_KEY must be str"),
            ([], "REMEMBER_COOKIE_PASETO_KEY must be str"),
        ],
    )
    def test_login_manager_with_invalid_type_of_key(self, app, key, msg):
        app.secret_key = "super secret string"
        app.config["REMEMBER_COOKIE_PASETO_KEY"] = key

        with pytest.raises(TypeError) as err:
            PasetoLoginManager(app)
            pytest.fail("PasetoLoginManager() should fail.")
        assert msg in str(err.value)

    def test_login_manager_without_secret_key(self, app):
        # app.secret_key = "super secret string"
        new_login_manager(app)

        with app.test_client() as c:
            res = c.post(
                "/login",
                data=dict(email="foo@bar.example", password="mysecret"),
                follow_redirects=True,
            )
            assert res.status_code == 500

    def test_login_manager_with_invalid_key(self, app):
        app.secret_key = "not 32bytes secret for v2"
        app.config["REMEMBER_COOKIE_PASETO_VERSION"] = 2
        new_login_manager(app)

        with app.test_client() as c:
            res = c.post(
                "/login",
                data=dict(email="foo@bar.example", password="mysecret"),
                follow_redirects=True,
            )
            assert res.status_code == 500
