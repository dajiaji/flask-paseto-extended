import json
import typing as t

import flask
from flask import _request_ctx_stack, request
from pyseto import Key, Paseto

from .config import PASETO_VERSIONS_ACCEPTABLE
from .token import Token

PASETO_DEFAULT_SKEW: int = 0
PASETO_DEFAULT_DESERIALIZER: t.Any = json


def _default_token_loader(cb: flask.Request) -> str:
    raise NotImplementedError("token_loader must be defined.")


def _default_verification_error_handler() -> flask.Response:
    raise NotImplementedError("verification_error_handler must be defined.")


class PasetoVerifier(object):
    def __init__(self, app=None, add_context_processor=True):

        if app is not None:
            self.init_app(app, add_context_processor)

        # Callbacks
        self._token_loader: t.Callable[[flask.Request], str] = _default_token_loader
        self._verification_error_handler: t.Callable[
            [None], flask.Response
        ] = _default_verification_error_handler

    def init_app(self, app, add_context_processor=True):
        """
        Configures an Flask application to use this PasetoVerifier.
        """
        app.paseto_verifier = self

        # _skew
        self._skew: int = app.config.get("PASETO_SKEW", PASETO_DEFAULT_SKEW)
        if not isinstance(self._skew, int) or self._skew < 0:
            raise ValueError("PASETO_SKEW must be int (>= 0).")

        # _deserializer
        self._deserializer: t.Any = app.config.get(
            "PASETO_DESERIALIZER", PASETO_DEFAULT_DESERIALIZER
        )
        if not hasattr(self._deserializer, "loads") or not callable(
            self._deserializer.loads
        ):
            raise ValueError("PASETO_DESERIALIZER must have a callable 'loads'.")

        # _keys
        keys: list = app.config.get("PASETO_PUBLIC_KEYS", [])
        if not keys:
            raise ValueError("PASETO_PUBLIC_KEYS must be set.")
        self._keys: list = []
        self._issuers: dict = {}
        key: t.Any = None
        kid: bytes = b""
        for k in keys:
            if "paserk" in k:
                try:
                    key = Key.from_paserk(k["paserk"])
                except Exception as err:
                    raise ValueError("Invalid PASERK data.") from err
                if key.purpose == "local":
                    raise ValueError("A local key is not allowed.")
            else:
                if "version" not in k:
                    raise ValueError(
                        "A key object must have a 'paserk' or a pair of 'version' and 'key'."
                    )
                if not isinstance(k["version"], int):
                    raise ValueError("A 'version' in PASETO_PUBLIC_KEYS must be int.")
                if k["version"] not in PASETO_VERSIONS_ACCEPTABLE:
                    raise ValueError(f"Invalid PASETO version: {k['version']}.")
                if "key" not in k:
                    raise ValueError(
                        "A key object must have a 'paserk' or a pair of 'version' and 'key'."
                    )
                try:
                    key = Key.new(k["version"], "public", k["key"])
                except Exception as err:
                    raise ValueError("A 'key' must be a PEM formatted key.") from err
            self._keys.append(key)
            if "iss" in k:
                if not isinstance(k["iss"], str):
                    raise ValueError("An 'iss' must be str.")
                kid = key.to_paserk_id()
                self._issuers[kid] = k["iss"]

        self._paseto = Paseto.new(leeway=self._skew)
        return

    def token_loader(
        self, cb: t.Callable[[flask.Request], str]
    ) -> t.Callable[[flask.Request], str]:
        """ """
        self._token_loader = cb
        return self.token_loader_callback

    @property
    def token_loader_callback(self):
        """ """
        return self._token_loader

    def verification_error_handler(
        self, cb: t.Callable[[None], flask.Response]
    ) -> t.Callable[[None], flask.Response]:
        """ """
        self._verification_error_handler = cb
        return self.verification_error_handler_callback

    @property
    def verification_error_handler_callback(self):
        """ """
        return self._verification_error_handler

    def _load_and_verify(self):

        ctx = _request_ctx_stack.top
        token = self._token_loader(request)
        if not token:
            ctx.paseto = Token(
                False,
                error=Exception(
                    "A PASETO token could not be loaded via 'token_loader'."
                ),
            )
            return
        try:
            t = self._paseto.decode(self._keys, token, deserializer=self._deserializer)
            ctx.paseto = Token(True, t.version, t.purpose, t.payload, t.footer)
        except Exception as err:
            ctx.paseto = Token(False, error=err)
        return
