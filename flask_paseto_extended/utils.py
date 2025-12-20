import typing as t

import pyseto
from flask import current_app
from pyseto import Key


def encode_cookie(payload: str | bytes, key: str | bytes | None = None) -> str:
    if current_app.secret_key is None and key is None:
        raise ValueError("Either app.secret_key or key should be specified")

    k: str | bytes | None = key if key is not None else current_app.secret_key
    if k is None:
        raise ValueError("A valid secret key must be provided")
    version = t.cast(int, getattr(getattr(current_app, "login_manager", None), "paseto_version", 4))
    enc_key = Key.new(version, "local", k)
    encoded: bytes = t.cast(bytes, pyseto.encode(enc_key, payload))
    return encoded.decode("utf-8")


def decode_cookie(cookie: str | bytes, key: str | bytes | None = None) -> str:
    k: str | bytes | None = key if key is not None else current_app.secret_key
    if k is None:
        raise ValueError("A valid secret key must be provided")
    version = t.cast(int, getattr(getattr(current_app, "login_manager", None), "paseto_version", 4))
    dec_key = Key.new(version, "local", k)
    payload = pyseto.decode(dec_key, cookie).payload
    if isinstance(payload, str):
        return payload
    if isinstance(payload, bytes):
        return payload.decode("utf-8")
    return str(payload)
