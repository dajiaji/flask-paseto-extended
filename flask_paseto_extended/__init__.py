from .cookie_session import PasetoCookieSessionInterface
from .exceptions import DecodeError, EncodeError, FlaskPasetoError
from .issuer import PasetoIssuer
from .login_manager import PasetoLoginManager
from .token import Token, current_paseto, paseto_required
from .verifier import PasetoVerifier

__version__ = "0.3.1"
__title__ = "Flask PASETO Extended"
__description__ = "PASETO (Platform-Agnostic Security Tokens) for Flask applications."
__url__ = "https://github.com/dajiaji/flask-paseto-extended"
__uri__ = __url__
__doc__ = __description__ + " <" + __uri__ + ">"
__author__ = "Ajitomi Daisuke"
__email__ = "dajiaji@gmail.com"
__license__ = "MIT"
__copyright__ = "Copyright 2021 Ajitomi Daisuke"
__all__ = [
    "PasetoCookieSessionInterface",
    "PasetoLoginManager",
    "PasetoIssuer",
    "PasetoVerifier",
    "Token",
    "current_paseto",
    "paseto_required",
    "FlaskPasetoError",
    "EncodeError",
    "DecodeError",
]
