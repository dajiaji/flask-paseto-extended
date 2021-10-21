import flask
import flask_login
import pytest

from flask_paseto_extended import PasetoLoginManager


@pytest.fixture(scope="function")
def app():

    app = flask.Flask(__name__)
    app.secret_key = "super secret string"
    login_manager = PasetoLoginManager(app)

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


class TestPasetoLoginManager:
    """
    Tests for PasetoLoginManager.
    """

    def test_sample_login_manager(self, app):

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
