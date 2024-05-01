"""
Test file for app/app.py    
"""

import sys
import pytest
import unittest
import mongomock

sys.path.append("app")
from app import app

# TODO: Implement Mock data base so the tests don't corrupt the data from the real db.
# Maybe create a collection for solely testing?

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
