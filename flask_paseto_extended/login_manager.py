from datetime import datetime, timedelta

from flask import current_app, session
from flask_login import (
    COOKIE_DURATION,
    COOKIE_HTTPONLY,
    COOKIE_NAME,
    COOKIE_SECURE,
    LoginManager,
    user_loaded_from_cookie,
)

from .utils import decode_cookie, encode_cookie

COOKIE_SAMESITE = None
DEFAULT_REMEMBER_COOKIE_PASETO_VERSION = 4


class PasetoLoginManager(LoginManager):
    def init_app(self, app, add_context_processor=True):

        super().init_app(app, add_context_processor)

        self.paseto_version = app.config.get(
            "REMEMBER_COOKIE_PASETO_VERSION", DEFAULT_REMEMBER_COOKIE_PASETO_VERSION
        )
        if not isinstance(self.paseto_version, int):
            raise TypeError("REMEMBER_COOKIE_PASETO_VERSION must be int")
        if self.paseto_version not in [1, 2, 3, 4]:
            raise ValueError("REMEMBER_COOKIE_PASETO_VERSION must be 1, 2, 3 or 4")

        self._remember_cookie_key = app.config.get("REMEMBER_COOKIE_PASETO_KEY", None)
        if not isinstance(self._remember_cookie_key, (type(None), str)):
            raise TypeError("REMEMBER_COOKIE_PASETO_KEY must be str")

    def _set_cookie(self, response):

        # cookie settings
        config = current_app.config
        cookie_name = config.get("REMEMBER_COOKIE_NAME", COOKIE_NAME)
        domain = config.get("REMEMBER_COOKIE_DOMAIN")
        path = config.get("REMEMBER_COOKIE_PATH", "/")

        secure = config.get("REMEMBER_COOKIE_SECURE", COOKIE_SECURE)
        httponly = config.get("REMEMBER_COOKIE_HTTPONLY", COOKIE_HTTPONLY)
        samesite = config.get("REMEMBER_COOKIE_SAMESITE", COOKIE_SAMESITE)

        if "_remember_seconds" in session:
            duration = timedelta(seconds=session["_remember_seconds"])
        else:
            duration = config.get("REMEMBER_COOKIE_DURATION", COOKIE_DURATION)

        # prepare data
        data = encode_cookie(str(session["_user_id"]), self._remember_cookie_key)

        if isinstance(duration, int):
            duration = timedelta(seconds=duration)

        try:
            expires = datetime.utcnow() + duration
        except TypeError as err:
            raise TypeError(
                "REMEMBER_COOKIE_DURATION must be datetime.timedelta"
            ) from err

        # actually set it
        response.set_cookie(
            cookie_name,
            value=data,
            expires=expires,
            domain=domain,
            path=path,
            secure=secure,
            httponly=httponly,
            samesite=samesite,
        )
        return

    def _load_user_from_remember_cookie(self, cookie):

        user_id = decode_cookie(cookie, self._remember_cookie_key)
        if user_id is None:
            return None
        session["_user_id"] = user_id
        session["_fresh"] = False
        user = None
        if self._user_callback:
            user = self._user_callback(user_id)
        if user is not None:
            app = current_app._get_current_object()
            user_loaded_from_cookie.send(app, user=user)
        return user
