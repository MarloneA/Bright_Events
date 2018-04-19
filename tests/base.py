import unittest
import os
import json
from app import create_app, db, version
from app.models import User, Event
from flask import jsonify

class BaseTestCase(unittest.TestCase):

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app(config_name="testing")
        self.client = self.app.test_client
        self.user_data = {
            'firstName':'Test',
            'lastName':'Admin',
            'email': 'admin@admin.com',
            'password': 'admin'
        }
        self.login_data = {
            'email': 'admin@admin.com',
            'password': 'admin'
        }
        self.empty_data = {
            'firstName': ' ',
            'lastName': ' ',
            'email': '  ',
            'password': '  '
        }
        self.int_data = {
            'firstName':3,
            'lastName':3,
            'email': 'admin@admin.com',
            'password': 'admin'
        }

        self.event_data = {
            'title':'daraja',
            'category': 'showcase',
            'location': 'nairobi',
            'date_of_event':'22 March 2018',
            'description':'a small intimate setting for singers, musicians and poetry collaborations'
        }
        self.empty_title = {
            'title':'  ',
            'category': 'showcase',
            'location': 'nairobi',
            'date_of_event':'22 March 2018',
            'description':'a small intimate setting for singers, musicians and poetry collaborations'
        }
        self.int_title = {
            'title':45,
            'category': 'showcase',
            'location': 'nairobi',
            'date_of_event':'22 March 2018',
            'description':'a small intimate setting for singers, musicians and poetry collaborations'
        }
        self.update_data = {
            "title":"it",
            "location":"derry",
            "category":"horror",
            'date_of_event':'22 March 2018',
            "description": "Billy Denbrough beats the devil"
        }
        self.filter_data = [
            {
            "title":"rasgueado",
            "location":"derry",
            "category":"music",
            'date_of_event':'22 March 2018',
            "description":"Come see the mariachi"
            },
            {
            "title":"it",
            "location":"derry",
            "category":"horror",
            'date_of_event':'22 March 2018',
            "description":"Come see pennywise the clown in action"
            },
            {
            "title":"flam",
            "location":"nairobi",
            "category":"music",
            'date_of_event':'22 March 2018',
            "description":"Come see the king of flam"
            }
        ]

        # binds the app to the current context
        with self.app.app_context():
            # create all tables
            db.create_all()


    def register_helper(self, par):
        """
        helper method for client registration
        """

        res = self.client().post(
                version+'/auth/register',
                data=json.dumps(par)
                )
        return res

    def login_helper(self, par):
        """
        Helper method for client login
        """

        res = self.client().post(
                version+'/auth/login',
                data=json.dumps(par)
                )

        return res

    def logout_helper(self, par):
        """
        helper method for logout
        """

        res = self.client().post(
            version+'/auth/logout',
            headers={"x-access-token":par['x-access-token']}
        )

        return res

    # def register_user(self):
    #     """
    #     This helper method helps register a test user.
    #     """
    #
    #     return self.client().post(version+'/auth/register', data=json.dumps(self.user_data))


    def login_user(self, email="admin@admin.com", password="admin"):
        """
        This helper method helps log in a test user.
        """
        user_data = {
            'email': email,
            'password': password
        }
        return self.client().post(version+'/auth/login', data=json.dumps(user_data))

    def reset_password_helper(self):
        """
        This helper method helps reset passwords
        """

        new_credentials = {
            'email':self.user_data['email'],
            'oldPassword':self.user_data['password'],
            'newPassword':'paramour'
        }

        res = self.client().post(
            version+'/auth/reset-password',
            data=json.dumps(new_credentials)
        )

        return res

    def set_headers(self, par):
        """
        helper method that sets request headers
        """

        token = json.loads(par.data.decode())['x-access-token']

        print(par)

        head = {
            "x-access-token":token,
            "Content-Type":"application/json"
            }

        return head

    def create_event_helper(self, head, dtparam):
        """
        helper method for creating evnts
        """

        res = self.client().post(
                version+'/events',
                headers=head,
                data=json.dumps(dtparam)
                )

        return res

    def reserve_event_helper(self, head, email):
        """
        Helper method for reserving guests
        """

        res = self.client().post(
                version+'/event/1/rsvp',
                headers=head,
                data=json.dumps({"email":email})
                )

        return res



    def tearDown(self):
        """teardown all initialized variables."""
        with self.app.app_context():
            # drop all tables
            db.session.remove()
            db.drop_all()
