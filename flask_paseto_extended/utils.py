import pyseto
from flask import current_app
from pyseto import Key


def encode_cookie(payload, key=None):

    if not current_app.secret_key and not key:
        raise ValueError("Either app.secret_key or key should be specified")

    k = current_app.secret_key if not key else key
    enc_key = Key.new(current_app.login_manager.paseto_version, "local", k)
    return pyseto.encode(enc_key, payload)


def decode_cookie(cookie, key=None):

    k = current_app.secret_key if not key else key
    dec_key = Key.new(current_app.login_manager.paseto_version, "local", k)
    return pyseto.decode(dec_key, cookie).payload.decode("utf-8")
