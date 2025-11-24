import typing as t

import pyseto
from flask import Flask, Request, Response
from flask.json.tag import TaggedJSONSerializer
from flask.sessions import SecureCookieSession, SessionInterface, SessionMixin
from pyseto import Key


class PasetoCookieSessionInterface(SessionInterface):
    def __init__(self, paseto_version: int = 4):
        if not isinstance(paseto_version, int) or paseto_version not in [1, 2, 3, 4]:
            raise ValueError(f"Invalid PASETO version: {paseto_version}")

        self._paseto_version = paseto_version
        self._serializer = TaggedJSONSerializer()

    def open_session(self, app: Flask, request: Request) -> t.Optional[SessionMixin]:
        """
        Opens a session.
        """
        if app.secret_key is None:
            return None
        secret_key = app.secret_key

        val = request.cookies.get(self.get_cookie_name(app))
        if not val:
            return SecureCookieSession()

        # max_age = int(app.permanent_session_lifetime.total_seconds())

        try:
            dec_key = Key.new(self._paseto_version, "local", secret_key)
            decoded_payload = pyseto.decode(dec_key, val).payload
            if isinstance(decoded_payload, str):
                serialized_session = decoded_payload
            elif isinstance(decoded_payload, bytes):
                serialized_session = decoded_payload.decode("utf-8")
            else:
                serialized_session = str(decoded_payload)
            return SecureCookieSession(self._serializer.loads(serialized_session))
        except Exception:
            return SecureCookieSession()

    def save_session(self, app: Flask, session: SessionMixin, response: Response) -> None:
        """
        Saves a session.
        """
        name = self.get_cookie_name(app)
        domain = self.get_cookie_domain(app)
        path = self.get_cookie_path(app)
        secure = self.get_cookie_secure(app)
        samesite = self.get_cookie_samesite(app)

        if not session:
            if session.modified:
                response.delete_cookie(name, domain=domain, path=path, secure=secure, samesite=samesite)
            return

        if session.accessed:
            response.vary.add("Cookie")

        if not self.should_set_cookie(app, session):
            return

        httponly = self.get_cookie_httponly(app)
        expires = self.get_expiration_time(app, session)
        secret_key = app.secret_key
        if secret_key is None:
            return
        enc_key = Key.new(self._paseto_version, "local", secret_key)
        serialized_session = self._serializer.dumps(dict(session))
        val = pyseto.encode(enc_key, serialized_session).decode("ascii")
        response.set_cookie(
            name,
            val,
            expires=expires,
            httponly=httponly,
            domain=domain,
            path=path,
            secure=secure,
            samesite=samesite,
        )
        return
