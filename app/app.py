""" code related to the app goes here """

from flask import Flask, render_template, redirect, request, url_for
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
cxn = pymongo.MongoClient(os.getenv("MONGO_URI"))
db = cxn[os.getenv("MONGO_DB")]  # store a reference to the database

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
                return redirect(url_for("profile", profileName=username))
            else:
                return render_template("login.html", username_dne=False, wrong_pw=True)
        # For demonstration, redirect to profile page after login
        return render_template("login.html", username_dne=True, wrong_pw=False)
    return render_template("login.html", username_dne=False, wrong_pw=False)


# profile page
@app.route("/profile/<profileName>")
def profile(profileName):
    user = db.Users.find_one({"username": profileName})
    pic = user["currentPFP"]
    return render_template("profile.html", pic=pic, profileName=profileName)


# account creation page
@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        if db.Users.find_one({"username": username}) != None:
            return redirect("/signup")  # Username taken, should display error
        else:
            db.Users.insert_one(
                {
                    "username": username,
                    "passHash": sha256(password.encode("utf-8")).hexdigest(),
                    "currentPFP": "https://www.shutterstock.com/image-vector/blank-avatar-photo-place-holder-600nw-1095249842.jpg",
                }
            )
            return redirect("/login")  # add user and send them to sign in
    return render_template("signup.html", username_taken=True)


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
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
