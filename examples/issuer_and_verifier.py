import flask
from flask import jsonify, make_response

from flask_paseto_extended import (
    PasetoIssuer,
    PasetoVerifier,
    current_paseto,
    paseto_required,
)

# Mock user database.
users = {"foo@bar.example": {"password": "mysecret"}}


app = flask.Flask(__name__)

# Configurations for PasetoIssuer.
app.config["PASETO_ISS"] = "https://issuer.example"
app.config["PASETO_PRIVATE_KEYS"] = [
    {
        "version": 4,
        "key": "-----BEGIN PRIVATE KEY-----\nMC4CAQAwBQYDK2VwBCIEILTL+0PfTOIQcn2VPkpxMwf6Gbt9n4UEFDjZ4RuUKjd0\n-----END PRIVATE KEY-----",
    },
]
# app.config["PASETO_USE_ISS"] = True
# app.config["PASETO_USE_IAT"] = True
# app.config["PASETO_EXP"] = 3600
# app.config["PASETO_SERIALIZER"] = json # or e.g., cbor2
issuer = PasetoIssuer(app)


# Configurations for PasetoVerifier.
app.config["PASETO_PUBLIC_KEYS"] = [
    {
        "iss": "https://issuer.exmaple",
        "version": 4,
        "key": "-----BEGIN PUBLIC KEY-----\nMCowBQYDK2VwAyEAHrnbu7wEfAP9cGBOAHHwmH4Wsot1ciXBHwBBXQ4gsaI=\n-----END PUBLIC KEY-----",
    },
]
# app.config["PASETO_SKEW"] = 60  # in seconds
# app.config["PASETO_DESERIALIZER"] = json # or e.g., cbor2
verifier = PasetoVerifier(app)


@verifier.token_loader
def token_loader(req: flask.Request):
    return req.cookies.get("paseto", None)


@verifier.verification_error_handler
def verification_error_handler():
    resp = make_response("Unauthorized")
    resp.delete_cookie("paseto", httponly=True)
    return resp


@app.route("/login", methods=["GET", "POST"])
def login():
    if flask.request.method == "GET":
        return """
               <form action='login' method='POST'>
                <input type='text' name='email' id='email' placeholder='email'/>
                <input type='password' name='password' id='password' placeholder='password'/>
                <input type='submit' name='submit'/>
               </form>
               """

    email = flask.request.form["email"]
    if flask.request.form["password"] != users[email]["password"]:
        return "Bad login"

    token = issuer.issue(payload={"user": {"email": email}})
    resp = flask.redirect(flask.url_for("protected"))
    # NOTE: MUST add secure=True in production.
    resp.set_cookie("paseto", token, httponly=True)
    return resp


@app.route("/logout")
def logout():
    resp = make_response("Logged out")
    resp.delete_cookie("paseto", httponly=True)
    return resp


@app.route("/protected/users/self")
@paseto_required()
def protected():
    return jsonify(current_paseto.payload["user"])
