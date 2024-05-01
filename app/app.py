""" code related to the app goes here """

from flask import Flask, render_template, redirect, request, url_for, flash
from flask_pymongo import PyMongo
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from datetime import datetime

import pymongo
from bson.objectid import ObjectId
from dotenv import load_dotenv
import flask_login
import os
from hashlib import sha256

load_dotenv()  # take environment variables from .env.

# create app
app = Flask(__name__)
app.secret_key = "Gauss"
# Setup login
login_manager = flask_login.LoginManager()

login_manager.init_app(app)

# connect to the database
cxn = pymongo.MongoClient(
    os.getenv("MONGO_URI", "mongodb://localhost:27017/"),
    tlsAllowInvalidCertificates=True,
)
db = cxn[os.getenv("MONGO_DB", "default_db")]  # store a reference to the database

try:
    # verify the connection works by pinging the database
    cxn.admin.command("ping")  # The ping command is cheap and does not require auth.
    print(" *", "Connected to MongoDB!")  # if we get here, the connection worked!
except Exception as e:
    # the ping command failed, so the connection is not available.
    print(" * MongoDB connection error:", e)  # debug


class User(flask_login.UserMixin):
    pass


@app.context_processor
def inject_username():
    if hasattr(flask_login.current_user, "id"):
        return dict(username=flask_login.current_user.id)
    return dict(username=None)


@login_manager.user_loader
def user_loader(username):
    if db.Users.find_one({"username": username}) == None:
        return

    user = User()
    user.id = username
    return user


@login_manager.request_loader
def request_loader(request):
    username = request.form.get("username")
    if db.Users.find_one({"username": username}) == None:
        return

    user = User()
    user.id = username
    return user


@app.route("/")
def index():
    print("Index route is being called")
    return render_template("index.html")


# login page
@app.route("/login")
# login page
@app.route("/login", methods=["GET", "POST"])  # Add methods=['GET', 'POST']
def login():
    if request.method == "POST":
        # Process login form data
        username = request.form.get("username")
        password = request.form.get("password")
        # Add your authentication logic here
        account = db.Users.find_one({"username": username})
        if account != None:
            if account["passHash"] == sha256(password.encode("utf-8")).hexdigest():
                user = User()
                user.id = username
                flask_login.login_user(user)
                return redirect(url_for("profile"))
            else:
                return render_template("login.html", username_dne=False, wrong_pw=True)
        # For demonstration, redirect to profile page after login
        return render_template("login.html", username_dne=True, wrong_pw=False)
    return render_template("login.html", username_dne=False, wrong_pw=False)


# profile page
@app.route("/profile")
@flask_login.login_required
def profile():
    currentUser = flask_login.current_user.id
    user = db.Users.find_one({"username": currentUser})
    pic = user["currentPFP"]
    score = user["score"]
    return render_template(
        "profile.html", pic=pic, profileName=currentUser, scoreDisp=score
    )


# account creation page
@app.route("/signup", methods=["GET", "POST"])
def signup():  # pragma: no cover
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        if db.Users.find_one({"username": username}) != None:
            return render_template("signup.html", username_taken=True)  # Username taken
        else:
            db.Users.insert_one(
                {
                    "username": username,
                    "passHash": sha256(password.encode("utf-8")).hexdigest(),
                    "currentPFP": "https://www.shutterstock.com/image-vector/blank-avatar-photo-place-holder-600nw-1095249842.jpg",
                    "friends": [],
                    "score": 0,
                }
            )
            return redirect("/login")  # add user and send them to sign in
    return render_template("signup.html", username_taken=False)


@app.route("/friends", methods=["GET", "POST"])
@flask_login.login_required
def friends():
    currentUser = flask_login.current_user.id
    user = db.Users.find_one({"username": currentUser})
    friends = user["friends"]
    friendData = []  # List to store friend data including username and score
    for friend_username in friends:
        friend = db.Users.find_one({"username": friend_username})
        if friend:  # Check if friend exists
            friendData.append(friend_username + " (" + str(friend["score"]) + " wins)")
    if request.method == "GET":
        return render_template("friends.html", friendList=friendData)
    else:
        target = request.form.get("target")
        if db.Users.find_one({"username": target}) != None:
            if target in friends:
                friends.remove(target)
            else:
                friends.append(target)
            db.Users.update_one(
                {"username": currentUser}, {"$set": {"friends": friends}}, upsert=True
            )
        else:
            flash("User not Found")
        friendData = []  # List to store friend data including username and score
        for friend_username in friends:
            friend = db.Users.find_one({"username": friend_username})
            if friend:  # Check if friend exists
                friendData.append(
                    friend_username + " (" + str(friend["score"]) + " wins)"
                )
        return render_template("friends.html", friendList=friendData)


@app.route("/game")
def game():
    print("routing")
    return render_template("game.html")


@app.route("/scored", methods=["GET", "POST"])
@flask_login.login_required
def scored():
    currentUser = flask_login.current_user.id
    user = db.Users.find_one({"username": currentUser})
    score = user["score"]
    if request.method == "POST":
        score += 1
        db.Users.update_one(
            {"username": currentUser}, {"$set": {"score": score}}, upsert=True
        )
        return "200"
    else:
        return render_template("score.html")


@app.route("/logout")
def logout():
    flask_login.logout_user()
    return redirect("/login")


# Error pages
@app.errorhandler(404)
@app.errorhandler(500)
def error_page(error):
    error_code = error.code
    if error_code == 404:
        error_description = "Page not found"
    else:
        error_description = "Internal server error"
    return (
        render_template(
            "error.html", error_code=error_code, error_description=error_description
        ),
        error_code,
    )


# run app
if __name__ == "__main__":  # pragma: no cover
    app.run(host="0.0.0.0", port=5000)
