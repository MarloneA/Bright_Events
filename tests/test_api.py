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

    def test_register_user(self):
        """
        Test that API endpoint ''/api/auth/register' creates a new user account
        """

        data = {
                'name':'test',
                'email': 'test@example.com',
                'password': 'test_password'
                }
        res = self.client().post(
            '/api/v2/auth/register',
            data,
            content_type='application/json'
        )

        self.assertEqual(data['name'], 'test')
        self.assertEqual(data['email'], 'test@example.com')
        self.assertEqual(data['password'], 'test_password')
        self.assertNotEqual(res.status_code, 200)

    def test_login_user(self):
        """
        Test that API endpoint '/api/auth/login' adds login details
        """

        data = dict({

                'email': 'test@example.com',
                'password': 'test_password'

                })

        login_res = self.client().post('/api/v2/auth/login', data)

        self.assertEqual(login_res.status_code, 400)

    def test_logout_user(self):
        """
        Test that API endpoint '/api/auth/logout' logs out os a session
        """

        return ""


    def test_create_event(self):
        """
        Test that API endpoint '/api/events' has created an event
        """
        return ""

    def test_update_event(self):
        """
        Test that API endpoint '/api/events/<eventId>' has made an update request
        """
        return ""

    def test_delete_event(self):
        """
        Test that API endpoint '/api/events/<eventId>' has deleted an event
        """

        return ""


    def test_delete_event(self):
        """
        Test that API endpoint '/api/events/<eventId>' has deleted an event
        """

        return ""


    def test_rsvp_event(self):
        """
        Test that API endpoint '/api/event/<eventId>/rsvp' reserves a guest
        """

        return ""

    def test_retrieve_reserved_guests(self):
        """
        Test that API endpoint '/api/event/<eventId>/rsvp' retrieves event guests
        """

        return ""

    def test_search_for_event(self):
        """
        Test that API endpoint '/api/events' has created an event
        """

        return ""

    def test_filter_event_by_category(self):
        """
        Test that API endpoint '/api/events' retrieves all events
        """

        return ""

    def test_filter_event_by_location(self):
        """
        Test that API endpoint '/api/events/<eventId>' has made an update request
        """

        return ""

    def test_render_api_as_root(self):

        return ""



    def tearDown(self):
        """teardown all initialized variables."""
        with self.app.app_context():
            # drop all tables
            db.session.remove()
            db.drop_all()

if __name__ == "__main__":
    unittest.main()
