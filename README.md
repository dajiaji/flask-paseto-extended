# Flask PASETO Extended

Flask-PASETO-Extended is a Flask extension to use [PASETO (Platform-Agnostic Security Tokens)](https://paseto.io/).
It is built on top of [PySETO](https://github.com/dajiaji/pyseto) which is a PASETO implementation
and supports all of PASETO versions (`v4`, `v3`, `v2` and `v1`) and purposes (`local` and `public`).

Currently, we provide the following classes for using PASETO with Flask.

- `PasetoCookieSessionInterface`: Flask stores session information as a Cookie value.
  By using this class, you can serialize the session information as an encrypted PASETO.
- `PasetoLoginManager`: By using this class together with [Flask-Login](https://github.com/maxcountryman/flask-login),
  you can use PASETO for remember-me tokens which is also encoded into a Cookie value.
- `PasetoManager`: This class can be used for verifying public (signed) PASETO.
  It is suitable for using PASETO as API tokens.

## Installation

You can install Flask-PASETO-Extended with pip:

```py
$ pip install flask-paseto-extended
```

## Usage

Flask-PASETO-Extended provides three classes for each purpose.

### PasetoCookieSessionInterface

This class can be used as follows:

```py
import flask
from flask_paseto_extended import PasetoCookieSessionInterface

app = flask.Flask(__name__)
app.secret_key = 'super secret string'

# Use PASETO("v4" by default) for cookie sessions.
app.session_interface = PasetoCookieSessionInterface()
```

See [examples/cookie_session.py](https://github.com/dajiaji/flask-paseto-extended/blob/main/examples/cookie_session.py) for a sample code that actually works.

### PasetoLoginManager


This class can be used as follows:

```py
import flask
import flask_login
from flask_paseto_extended import PasetoLoginManager

app = flask.Flask(__name__)
app.secret_key = 'super secret string'

login_manager = PasetoLoginManager(app)
```

See [examples/login_manager.py](https://github.com/dajiaji/flask-paseto-extended/blob/main/examples/login_manager.py) for a sample code that actually works.

### PasetoManager

T.B.D.

## Contributing

We welcome all kind of contributions, filing issues, suggesting new features or sending PRs.
