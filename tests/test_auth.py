import unittest
import os
import json
import psycopg2
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
            'email': 'admin@admin.com',
            'password': 'admin'
        }
        self.login_data = {
            'email': 'admin@admin.com',
            'password': 'admin'
        }
        self.empty_data = {
            'name':'  ',
            'email': '  ',
            'password': '  '
        }
        self.int_data = {
            'name':3,
            'email': 'admin@admin.com',
            'password': 'admin'
        }


        # binds the app to the current context
        with self.app.app_context():
            # create all tables
            db.create_all()


    def register_helper(self, par):
        """
        helper method for client registration
        """

        res = self.client().post(
                '/api/v2/auth/register',
                data=json.dumps(par)
                )
        return res

    def login_helper(self, par):
        """
        Helper method for client login
        """

        res = self.client().post(
                '/api/v2/auth/login',
                data=json.dumps(par)
                )

        return res


    def test_register_user(self):
        """
        Test if a user can succesfully register an account
        """

        res = self.register_helper(self.user_data)

        self.assertEqual(res.status_code, 201)
        self.assertIn("registration succesfull", res.data)

    def test_register_user_with_spaces(self):
        """
        Test that a user cannot register with empty spaces
        """

        res = self.register_helper(self.empty_data)

        self.assertEqual(res.status_code, 400)
        self.assertIn("name/email/password fields cannot be empty", res.data)

    def test_register_with_name_as_integer(self):
        """
        Users should not register with names as integers
        """

        res = self.register_helper(self.int_data)

        self.assertEqual(res.status_code, 400)
        self.assertIn("name cannot be an integer", res.data)

    def test_if_account_is_already_registered(self):
        """
        Test if an account is already registered
        """

        res = self.register_helper(self.user_data)
        res = self.register_helper(self.user_data)

        self.assertEqual(res.status_code, 400)
        self.assertIn("Email has already been registered", res.data)

    def test_login(self):
        """
        Test if a user can login
        """

        res = self.register_helper(self.user_data)
        res = self.login_helper(self.login_data)

        self.assertEqual(res.status_code, 200)
        self.assertIn("Login succesfull", res.data)
        self.assertIn("x-access-token", res.data)


    def test_logout_user(self):
        """
        Test if a user has succesfully been logged out
        """

        res = self.register_helper(self.user_data)
        res = self.login_helper(self.login_data)

        to_json = json.loads(res.data)

        res = self.client().post(
            '/api/v2/auth/logout',
            headers={"x-access-token":to_json['x-access-token']}
        )

        self.assertEqual(res.status_code, 200)
        self.assertIn("Successfully logged out",res.data)



    def test_reset_password(self):
        """
        Test if a User can reset their password
        """

        res = self.register_helper(self.user_data)

        new_credentials = {
            'email':self.user_data['email'],
            'oldPassword':self.user_data['password'],
            'newPassword':'paramour'
        }

        res = self.client().post(
            '/api/v2/auth/reset-password',
            data=json.dumps(new_credentials)
        )

        self.assertEqual(res.status_code, 200)
        self.assertIn("password has been updated succesfully", res.data)


    def tearDown(self):
        """teardown all initialized variables."""
        with self.app.app_context():
            # drop all tables
            db.session.remove()
            db.drop_all()

if __name__ == "__main__":
    unittest.main()
