import unittest
import os
import json
from app import create_app, db
from app.models import User, Event

class TestAuth(unittest.TestCase):
    """
    This Class covers Authentication related tests
    """

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app(config_name="testing")
        self.client = self.app.test_client
        self.user_data = {
            'name':'Test Admin',
            'email': 'admin@Admin.com',
            'password': 'admin'
        }

        # binds the app to the current context
        with self.app.app_context():
            # create all tables
            db.create_all()

    def test_register_user(self):
        """
        Test if a user can succesfully register an account
        """

        return ""

    def test_if_account_is_already_registered(self):
        """
        Test if an account is already registered
        """

        return ""

    def test_login(self):
        """
        Test if a user can login
        """

        return ""

    def test_already_logged_in(self):
        """
        Test if a user is already logged in
        """

        return ""

    def test_logout_user(self):
        """
        Test if a user has succesfully been logged out
        """

        return ""

    def test_reset_password(self):
        """
        Test if a User can reset their password
        """

        return ""

    def tearDown(self):
        """teardown all initialized variables."""
        with self.app.app_context():
            # drop all tables
            db.session.remove()
            db.drop_all()

if __name__ == "__main__":
    unittest.main()
