"""
Test file for app/app.py    
"""

import sys
import os
from dotenv import load_dotenv
import pytest
import pymongo
import unittest

load_dotenv()

sys.path.append("app")
from app import app

cxn = pymongo.MongoClient(
    os.getenv("MONGO_URI", "mongodb://localhost:27017/"),
    tlsAllowInvalidCertificates=True,
)
db = cxn[os.getenv("MONGO_DB", "Tests")]  # store a reference to the database


class TestAppRoutes:
    """
    Class for testing web app
    """

    def setup_method(self):
        """Set up the test client for each test."""
        self.app = app.test_client()
        self.app.post("/signup", data={"username": "testuser", "password": "password"})

    def test_index_route(self):
        response = self.app.get("/")
        assert response.status_code == 200

    # Test login functionality
    def test_invalid_login(self):
        response = self.app.post(
            "/login",
            data={"username": "invalid_user", "password": "invalid_password"},
            follow_redirects=True,
        )
        assert b"Username does not exist" in response.data

    def test_valid_login(self):
        response = self.app.post(
            "/login",
            data={"username": "testuser", "password": "password"},
            follow_redirects=True,
        )
        assert b"Welcome" in response.data

    def test_logout(self):
        response = self.app.get("/logout", follow_redirects=True)
        assert b"Login" in response.data

    def test_profile_access(self):
        # Assume user must be logged in to access this
        with self.app:
            self.app.post(
                "/login",
                data=dict(username="testuser", password="password"),
                follow_redirects=True,
            )
            response = self.app.get("/profile")
            assert response.status_code == 200
            assert b"Welcome testuser" in response.data

    def test_game_route(self):
        response = self.app.get("/game")
        assert response.status_code == 200

    def test_error_handling(self):
        response = self.app.get("/nonexistent-route")
        assert response.status_code == 404

    def test_friends_route_post(self):
        # Add a user "frienduser" to the database
        self.app.post(
            "/signup", data={"username": "frienduser", "password": "password"}
        )

        self.app.post(
            "/login",
            data=dict(username="testuser", password="password"),
            follow_redirects=True,
        )

        # Send a POST request to /friends with "frienduser" as the target
        response = self.app.post("/friends", data={"target": "frienduser"})
        assert response.status_code == 200

        # Check if the friend is added
        response = self.app.get("/friends")
        assert b"frienduser" in response.data

    def test_score_route(self):
        # Log in as testuser and reset score, then POST
        self.app.post(
            "/login",
            data={"username": "testuser", "password": "password"},
            follow_redirects=True,
        )

        db.Users.update_one({"username": "testuser"}, {"$set": {"score": 0}})

        response = self.app.post("/scored")

        # Check if the response code is 200
        assert response.status_code == 200

        # Check if the score is updated
        user = db.Users.find_one({"username": "testuser"})
        assert user["score"] == 1
