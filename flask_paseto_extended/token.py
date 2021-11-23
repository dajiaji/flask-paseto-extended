import typing as t
from functools import wraps

from flask import _request_ctx_stack, current_app, has_request_context
from werkzeug.local import LocalProxy

from .exceptions import ConfigError


class Token(object):
    """
    The parsed token object which can be referred as ``current_paseto`` in the
    views decorated by ``@token_required``.
    """

    def __init__(
        self,
        is_verified: bool,
        version: str = "",
        purpose: str = "",
        payload: t.Union[bytes, dict] = b"",
        footer: t.Union[bytes, dict] = b"",
        error: t.Optional[Exception] = None,
    ):

        self._is_verified = is_verified
        self._version = version
        self._purpose = purpose
        self._payload = payload
        self._footer = footer
        self._error = error
        self._header = (version + "." + purpose + ".").encode("utf-8")
        return

    @property
    def is_verified(self) -> bool:
        """
        If it is ``True``, the token has been verified.
        """
        return self._is_verified

    @property
    def version(self) -> str:
        """
        The version of the token. It will be ``"v1"``, ``"v2"``, ``"v3"`` or ``"v4"``.
        """
        return self._version

    @property
    def purpose(self) -> str:
        """
        The purpose of the token. It will be ``"local"`` or ``"public"``.
        """
        return self._purpose

    @property
    def header(self) -> bytes:
        """
        The header of the token. It will be ``"<version>.<type>."``.
        For example, ``"v1.local."``.
        """
        return self._header

    @property
    def payload(self) -> t.Union[bytes, dict]:
        """
        The payload of the token which is a decoded binary string. It's not Base64 encoded data.
        """
        return self._payload

    @property
    def footer(self) -> t.Union[bytes, dict]:
        """
        The footer of the token which is a decoded binary string. It's not Base64 encoded data.
        """
        return self._footer

    @property
    def error(self) -> t.Union[Exception, None]:
        """
        If ``is_verified`` is ``True``, this property will be specified.
        """
        return self._error


current_paseto: Token = LocalProxy(lambda: _get_token())  # type: ignore


def paseto_required():
    """ """

    def wrapper(func):
        @wraps(func)
        def decorated_view(*args, **kwargs):

            if not hasattr(current_app, "paseto_verifier"):
                raise ConfigError("paseto_verifier is not set in the current_app.")

            if not current_paseto.is_verified:
                return current_app.paseto_verifier.verification_error_handler_callback()

            if not hasattr(current_app, "ensure_sync"):
                return func(*args, **kwargs)
            # ensure_sync is available in Flask >= 2.0
            return current_app.ensure_sync(func)(*args, **kwargs)

        return decorated_view

    return wrapper


def _get_token() -> Token:
    """ """
    if has_request_context() and not hasattr(_request_ctx_stack.top, "paseto"):
        current_app.paseto_verifier._load_and_verify()  # type: ignore

    return getattr(_request_ctx_stack.top, "paseto", None)
