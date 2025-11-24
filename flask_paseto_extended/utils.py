import pyseto
from flask import current_app
from pyseto import Key


def encode_cookie(payload, key=None):
    if not current_app.secret_key and not key:
        raise ValueError("Either app.secret_key or key should be specified")

    k = key if key else current_app.secret_key
    enc_key = Key.new(current_app.login_manager.paseto_version, "local", k)
    return pyseto.encode(enc_key, payload).decode("utf-8")


def decode_cookie(cookie, key=None):
    k = key if key else current_app.secret_key
    dec_key = Key.new(current_app.login_manager.paseto_version, "local", k)
    return pyseto.decode(dec_key, cookie).payload.decode("utf-8")
