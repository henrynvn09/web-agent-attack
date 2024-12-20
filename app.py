from flask import Flask, render_template, redirect, request, url_for, jsonify
from flask_sqlalchemy import SQLAlchemy

from routes import user, session, transfer, gift

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config['SESSION_COOKIE_SAMESITE'] = 'Strict'


db = SQLAlchemy(app)


@app.route("/")
@app.route("/home")
@app.route("/index.html")
def home():
    auth = is_session_valid()
    return render_template("index.html", auth=auth), 200


@app.route("/register")
def register():
    auth = is_session_valid()
    if auth:
        return redirect(url_for("home")), 401
    return render_template("register.html", auth=auth), 200


@app.route("/login")
def login():
    auth = is_session_valid()
    if auth:
        return redirect(url_for("home")), 401
    return render_template("login.html", auth=auth), 200


@app.route("/logout")
def logout():
    auth = is_session_valid()
    if not auth:
        return redirect(url_for("login")), 401
    return render_template("logout.html", auth=auth), 200


@app.route("/profile")
def profile():
    auth = is_session_valid()
    if not auth:
        return redirect(url_for("login")), 401
    with app.app_context():
        from models.user import User

        token = request.cookies.get("session")
        session = db.session.query(Session).filter_by(token=token).first()
        session_user_id = session.user_id
        user = db.session.query(User).filter_by(id=session_user_id).first()

        if user is None:
            return redirect(url_for("login")), 401

    return render_template("profile.html", auth=auth, user=user), 200


@app.route("/shop")
def shop():
    auth = is_session_valid()
    if not auth:
        return redirect(url_for("login")), 401
    return render_template("shop.html", auth=auth), 200


@app.errorhandler(404)
def not_found(e):
    auth = is_session_valid()
    return render_template("404.html", auth=auth), 404


@app.route("/api/user", defaults={"id": None}, methods=["POST"])
@app.route("/api/user/<id>", methods=["GET", "PUT", "DELETE"])
def user_handler(id):
    if request.method == "GET" or request.method == "PUT" or request.method == "DELETE":
        if not is_session_valid():
            res = {"status": "Unauthorized."}
            return jsonify(res), 401
    return user.router(id)


@app.route("/api/session", defaults={"id": None}, methods=["POST"])
@app.route("/api/session/<id>", methods=["GET", "DELETE"])
def session_handler(id):
    if request.method == "GET" or request.method == "DELETE":
        if not is_session_valid():
            res = {"status": "Unauthorized."}
            return jsonify(res), 401
    return session.router(id)


with app.app_context():
    from models.user import User
    from models.session import Session, is_session_valid
    from models.gift import Gift

    db.metadata._add_table(User.__tablename__, None, User.__table__)
    db.metadata._add_table(Session.__tablename__, None, Session.__table__)
    db.metadata._add_table(Gift.__tablename__, None, Gift.__table__)

    db.create_all()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80)
