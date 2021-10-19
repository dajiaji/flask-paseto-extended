from .cookie_session import PasetoCookieSessionInterface
from .login_manager import PasetoLoginManager

__version__ = "0.0.1"
__title__ = "Flask PASETO Extended"
__description__ = "PASETO (Platform-Agnostic Security Tokens) for Flask applications."
__url__ = "https://github.com/dajiaji/flask-paseto"
__uri__ = __url__
__doc__ = __description__ + " <" + __uri__ + ">"
__author__ = "AJITOMI Daisuke"
__email__ = "ajitomi@gmail.com"
__license__ = "MIT"
__copyright__ = "Copyright 2021 AJITOMI Daisuke"
__all__ = [
    "PasetoCookieSessionInterface",
    "PasetoLoginManager",
]
