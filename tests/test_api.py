import unittest
import os
import json
from app import create_app, db
from app.models import User, Event

class TestAuth(unittest.TestCase):
    """
    This Class covers the main functionality of the API
    """

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app(config_name="testing")
        self.client = self.app.test_client
        self.user_data = {
            'name':'test',
            'email': 'test@example.com',
            'password': 'test_password'
        }

        # binds the app to the current context
        with self.app.app_context():
            # create all tables
            db.session.close()
            db.drop_all()
            db.create_all()


    def tearDown(self):
        """teardown all initialized variables."""
        with self.app.app_context():
            # drop all tables
            db.session.remove()
            db.drop_all()

if __name__ == "__main__":
    unittest.main()
