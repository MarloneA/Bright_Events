import json
from tests.base import BaseTestCase
from app import version

class TestAuth(BaseTestCase):
    """
    This Class covers Authentication related tests
    """

    def test_register_user(self):
        """
        Test if a user can succesfully register an account
        """

        res = self.register_helper(self.user_data)

        self.assertEqual(res.status_code, 201)
        self.assertIn("registration succesfull", res.data.decode())

    def test_register_user_with_spaces(self):
        """
        Test that a user cannot register with empty spaces
        """

        res = self.register_helper(self.empty_data)

        self.assertEqual(res.status_code, 400)
        self.assertIn("name/email/password fields cannot be empty", res.data.decode())

    def test_register_with_name_as_integer(self):
        """
        Users should not register with names as integers
        """

        res = self.register_helper(self.int_data)

        self.assertEqual(res.status_code, 400)
        self.assertIn("names cannot be integers", res.data.decode())

    def test_password_should_not_be_less_than_four_characters(self):
        """
        Test that a password should contain atleast four characters
        """

        self.user_data["password"]="123"
        res = self.register_helper(self.user_data)

        self.assertEqual(res.status_code, 400)
        self.assertIn("password should be at least 4 characters", res.data.decode())

    def test_if_account_is_already_registered(self):
        """
        Test if an account is already registered
        """

        self.register_helper(self.user_data)
        res = self.register_helper(self.user_data)

        self.assertEqual(res.status_code, 400)
        self.assertIn("Email has already been registered", res.data.decode())

    def test_login(self):
        """
        Test if a user can login
        """

        self.register_helper(self.user_data)
        res = self.login_helper(self.login_data)

        self.assertEqual(res.status_code, 200)
        self.assertIn("Login succesfull", res.data.decode())
        self.assertIn("token", res.data.decode())

    def test_login_with_wrong_email(self):
        """
        Test response for invalid email
        """

        self.register_helper(self.user_data)
        self.login_data["email"]="adm@admin.com"
        res = self.login_helper(self.login_data)

        self.assertEqual(res.status_code, 401)
        self.assertIn("Could not verify", res.data.decode())

    def test_login_with_wrong_password(self):
        """
        Test response for wrong password
        """

        self.register_helper(self.user_data)
        self.login_data["password"]="kdfj"
        res = self.login_helper(self.login_data)

        self.assertEqual(res.status_code, 401)
        self.assertIn("Incorrect password", res.data.decode())


    def test_login_request_has_a_json_object(self):
        """
        Test that the request syntax is a json object
        """

        self.register_helper(self.user_data)
        self.login_data=None
        res = self.login_helper(self.login_data)

        self.assertEqual(res.status_code, 401)
        self.assertIn("Invalid email/password", res.data.decode())

    def test_invalid_token_in_respnse_header(self):
        """
        Test if a token passed in the response header is invalid
        """

        self.register_helper(self.user_data)
        result = self.login_user()

        head = self.set_headers(result)
        head["token"]="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJwdWJsaWNfaWQiOjQsImV4cCI6MTUxODQyMDg4MX0.O3Zl80XmAIbaSQdf8RbP44TEyA4FxbkyniH2dwOdB44"
        res = self.create_event_helper(head, self.event_data)

        self.assertEqual(res.status_code, 401)
        self.assertIn("Token is invalid!", res.data.decode())


    def test_logout_user(self):
        """
        Test if a user has succesfully been logged out
        """

        self.register_helper(self.user_data)
        res = self.login_helper(self.login_data)

        to_json = json.loads(res.data.decode())
        res = self.logout_helper(to_json)

        self.assertEqual(res.status_code, 200)
        self.assertIn("Successfully logged out",res.data.decode())



    def test_reset_password(self):
        """
        Test if a User can reset their password
        """

        self.register_helper(self.user_data)
        res = self.reset_password_helper()

        self.assertEqual(res.status_code, 200)
        self.assertIn("password has been updated succesfully", res.data.decode())


if __name__ == "__main__":
    unittest.main()
