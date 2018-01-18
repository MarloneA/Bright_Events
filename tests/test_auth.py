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
            'email': 'admin@Admin.com',
            'password': 'admin'
        }

        # binds the app to the current context
        with self.app.app_context():
            # create all tables
            db.create_all()


    @staticmethod
    def charVarying():
        """
        Static method that changes character varying(50) to character varying(200)
        in the db to enable hashed passwords( method=sha256) to be stored
        """

        sqlstr = 'ALTER TABLE "user" ALTER COLUMN password TYPE character varying(200);'
        conn = psycopg2.connect("dbname=test_bev user=marlone911")
        cur = conn.cursor()
        cur.execute(sqlstr)

        conn.commit()

        cur.close()
        conn.close()



    def test_register_user(self):
        """
        Test if a user can succesfully register an account
        """

        self.charVarying()

        res = self.client().post(
                '/api/v2/auth/register',
                data=json.dumps(self.user_data)
                )

        self.assertEqual(res.status_code, 201)
        self.assertIn("registration succesfull", res.data)

    def test_if_account_is_already_registered(self):
        """
        Test if an account is already registered
        """

        self.charVarying()

        res = self.client().post(
                '/api/v2/auth/register',
                data=json.dumps(self.user_data)
                )

        self.assertEqual(res.status_code, 201)

        res = self.client().post(
                '/api/v2/auth/register',
                data=json.dumps(self.user_data)
                )

        self.assertEqual(res.status_code, 400)
        self.assertIn("Email has already been registered", res.data)

    def test_login(self):
        """
        Test if a user can login
        """

        self.charVarying()

        res = self.client().post(
                '/api/v2/auth/register',
                data=json.dumps(self.user_data)
                )
        self.assertEqual(res.status_code, 201)

        res = self.client().post(
                '/api/v2/auth/login',
                data=json.dumps({"email":self.user_data["email"], "password":self.user_data["password"]})
                )

        self.assertEqual(res.status_code, 200)
        self.assertIn("Login succesfull", res.data)
        self.assertIn("x-access-token", res.data)


    def test_already_logged_in(self):
        """
        Test if a user is already logged in
        """

        return ""


    def test_logout_user(self):
        """
        Test if a user has succesfully been logged out
        """

        self.charVarying()

        res = self.client().post(
                '/api/v2/auth/register',
                data=json.dumps(self.user_data)
                )
        self.assertEqual(res.status_code, 201)

        res = self.client().post(
                '/api/v2/auth/login',
                data=json.dumps({"email":self.user_data["email"], "password":self.user_data["password"]})
                )
        self.assertEqual(res.status_code, 200)

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

        self.charVarying()

        res = self.client().post(
                '/api/v2/auth/register',
                data=json.dumps(self.user_data)
                )
        self.assertEqual(res.status_code, 201)

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
