import json
import typing as t

from pyseto import Key, Paseto

from .config import PASETO_VERSIONS_ACCEPTABLE
from .exceptions import EncodeError

PASETO_DEFAULT_USE_ISS: bool = True
PASETO_DEFAULT_USE_IAT: bool = False
PASETO_DEFAULT_EXP: int = 3600
PASETO_DEFAULT_SERIALIZER: t.Any = json


class PasetoIssuer(object):
    def __init__(self, app=None, add_context_processor=True):

        if app is not None:
            self.init_app(app, add_context_processor)

    def init_app(self, app, add_context_processor=True):
        """
        Configures an Flask application to use this PasetoIssuer.
        """
        app.paseto_issuer = self

        # _iss
        self._iss = app.config.get("PASETO_ISS", "")
        if not self._iss:
            raise ValueError("PASETO_ISS must be set.")
        if not isinstance(self._iss, str):
            raise ValueError("PASETO_ISS must be str.")

        # _use_iss
        self._use_iss = app.config.get("PASETO_USE_ISS", PASETO_DEFAULT_USE_ISS)
        if not isinstance(self._use_iss, bool):
            raise ValueError("PASETO_USE_ISS must be bool.")

        # _use_iat
        self._use_iat = app.config.get("PASETO_USE_IAT", PASETO_DEFAULT_USE_IAT)
        if not isinstance(self._use_iat, bool):
            raise ValueError("PASETO_USE_IAT must be bool.")

        # _exp
        self._exp = app.config.get("PASETO_EXP", PASETO_DEFAULT_EXP)
        if not isinstance(self._exp, int) or self._exp < 0:
            raise ValueError("PASETO_EXP must be int (>= 0).")

        # _serializer
        self._serializer: t.Any = app.config.get(
            "PASETO_SERIALIZER", PASETO_DEFAULT_SERIALIZER
        )
        if not hasattr(self._serializer, "dumps") or not callable(
            self._serializer.dumps
        ):
            raise ValueError("PASETO_SERIALIZER must have a callable 'dumps'.")

        # _keys
        keys: list = app.config.get("PASETO_PRIVATE_KEYS", [])
        if not keys:
            raise ValueError("PASETO_PRIVATE_KEYS must be set.")
        self._keys: dict = {}
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
                    raise ValueError("A 'version' in PASETO_PRIVATE_KEYS must be int.")
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
            kid = key.to_paserk_id()
            self._keys[kid] = key

        self._paseto = Paseto.new(exp=self._exp, include_iat=self._use_iat)
        return

    def issue(self, payload: dict, kid: str = "") -> str:

        key = (
            self._keys[list(self._keys)[0]]
            if len(self._keys) == 1
            else self._keys.get(kid, None)
        )
        if not key:
            raise ValueError("A signing key is not found.")

        if self._use_iss:
            payload["iss"] = self._iss
        try:
            return self._paseto.encode(key, payload, serializer=self._serializer)
        except Exception as err:
            raise EncodeError("Failed to encode a token.") from err
