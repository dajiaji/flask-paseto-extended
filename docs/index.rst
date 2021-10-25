Welcome to Flask PASETO Extended
================================

Flask-PASETO-Extended provides following three classes to use `PASETO (Platform-Agnostic Security Tokens)`_ for Flask applications:

- `PasetoCookieSessionInterface`
    - Flask (`Flask.sessions`) stores session information as a Cookie value. By using this class, you can serialize the session information as a local (encrypted and then MACed) PASETO.
- `PasetoLoginManager`
    - By using this class together with `Flask-Login`_, you can use a local PASETO for remember-me tokens which is also encoded into a Cookie value.
- `PasetoVerifier`
    - This class can be used for verifying public (signed) PASETO. It is suitable for using PASETO as API tokens.

For encoding/decoding PASETO, we have adopted `PySETO`_, which is a PASETO implementation
and supports all of PASETO versions (`v4`, `v3`, `v2` and `v1`) and purposes (`local` and `public`).

Index
-----

.. toctree::
   :maxdepth: 2

   installation
   usage
   api
   changes

.. _`PASETO (Platform-Agnostic SEcurity TOkens)`: https://paseto.io/
.. _`PySETO`: https://github.com/dajiaji/pyseto
.. _`Flask-Login`: https://github.com/maxcountryman/flask-login
