import unittest
import os
import json
from app import create_app, db
from app.models import User, Event
from flask import jsonify
from test_auth import TestAuth

class TestEvent(unittest.TestCase):
    """
    This Class covers tests centered around CRUD operations of the API
    """

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app(config_name="testing")
        self.client = self.app.test_client
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

    def register_user(self, name="test", email="user@test.com", password="test1234"):
        """
        This helper method helps register a test user.
        """
        TestAuth.charVarying()

        user_data = {
            'name':name,
            'email': email,
            'password': password
        }
        return self.client().post('/api/v2/auth/register', data=json.dumps(user_data))


    def login_user(self, email="user@test.com", password="test1234"):
        """
        This helper method helps log in a test user.
        """
        user_data = {
            'email': email,
            'password': password
        }
        return self.client().post('/api/v2/auth/login', data=json.dumps(user_data))

    def set_headers(self, par):
        """
        helper method that sets request headers
        """

        token = json.loads(par.data.decode())['x-access-token']

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
                '/api/v2/events',
                headers=head,
                data=json.dumps(dtparam)
                )

        return res


    def test_create_event(self):
        """
        Test that API endpoint '/api/events' has created an event
        """

        self.register_user()
        result = self.login_user()

        head = self.set_headers(result)
        res = self.create_event_helper(head, self.event_data)

        self.assertEqual(res.status_code, 201)
        self.assertIn("new event has been created", res.data)


    def test_create_event_with_empty_title(self):
        """
        Tests users ahould not be able to create titles with empty spaces
        """

        self.register_user()
        result = self.login_user()

        head = self.set_headers(result)
        res = self.create_event_helper(head, self.empty_title)

        self.assertEqual(res.status_code, 400)
        self.assertIn("Please provide a valid title", res.data)

    def test_create_event_with_title_as_integer(self):
        """
        Test users should not be able to supply integers as titles
        """

        self.register_user()
        result = self.login_user()

        head = self.set_headers(result)
        res = self.create_event_helper(head, self.int_title)

        self.assertEqual(res.status_code, 400)
        self.assertIn("title cannot be an integer", res.data)

    def test_retrieve_events(self):
        """
        Test that APi endpoint retrieves all events
        """

        self.register_user()
        result = self.login_user()

        head = self.set_headers(result)
        res = self.create_event_helper(head, self.event_data)

        res = self.client().get('/api/v2/events/1/1', headers=head)

        to_json =  json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(to_json["total results"], 1)
        self.assertEqual(to_json["cur page"], 1)
        self.assertEqual(to_json["total pages"], 1)


    def test_update_event(self):
        """
        Test that API endpoint '/api/events/<eventId>' has made an update request
        """

        self.register_user()
        result = self.login_user()

        head = self.set_headers(result)
        self.create_event_helper(head, self.event_data)

        data=json.dumps(self.update_data)
        resU = self.client().put('/api/v2/events/1', headers=head, data=data)

        self.assertEqual(resU.status_code, 200)

    def test_delete_event(self):
        """
        Test that API endpoint '/api/events/<eventId>' has deleted an event
        """

        self.register_user()
        result = self.login_user()

        head = self.set_headers(result)
        self.create_event_helper(head, self.event_data)

        res = self.client().delete('api/v2/events/1', headers=head)
        self.assertEqual(res.status_code, 200)

        result = self.client().get('api/v2/events/it/1/1',headers=head)

        self.assertEqual(result.status_code, 400)
        self.assertIn("event not found!", result.data)

    def test_search_for_event(self):
        """
        Test that API endpoint '/api/events/<searchQuery>/<int:results/<int:page_num>' retrieves the requested event
        """

        self.register_user()
        result = self.login_user()

        head = self.set_headers(result)
        self.create_event_helper(head, self.event_data)

        res = self.client().get('/api/v2/events/daraja/5/1')
        to_json =  json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(len(to_json["Search_Results"]), 1)
        self.assertEqual(to_json["total results"], 1)
        self.assertEqual(to_json["total pages"], 1)
        self.assertEqual(to_json["cur page"], 1)
        self.assertEqual(to_json["prev page"], None)
        self.assertEqual(to_json["next page"], None)


    def test_filter_event_by_category(self):
        """
        Test that API endpoint '/api/v2/events/category/<category>' filters events by a category
        """
        self.register_user()
        result = self.login_user()

        head = self.set_headers(result)

        self.create_event_helper(head, self.filter_data[0])
        self.create_event_helper(head, self.filter_data[1])
        self.create_event_helper(head, self.filter_data[2])

        result = self.client().get('/api/v2/events/category/music/5/1')
        to_json =  json.loads(result.data)

        self.assertEqual(result.status_code, 200)
        self.assertEqual(len(to_json["Filter_Results"]), 2)
        self.assertEqual(to_json["total results"], 2)
        self.assertEqual(to_json["total pages"], 1)
        self.assertEqual(to_json["cur page"], 1)
        self.assertEqual(to_json["prev page"], None)
        self.assertEqual(to_json["next page"], None)


    def test_filter_event_by_location(self):
        """
        Test that API endpoint '/api/v2/events/location/<location>' filters events by location
        """

        self.register_user()
        result = self.login_user()

        head = self.set_headers(result)

        self.create_event_helper(head, self.filter_data[0])
        self.create_event_helper(head, self.filter_data[1])
        self.create_event_helper(head, self.filter_data[2])

        result = self.client().get('/api/v2/events/location/derry/5/1')
        to_json =  json.loads(result.data)

        self.assertEqual(result.status_code, 200)
        self.assertEqual(len(to_json["Filter_Results"]), 2)
        self.assertEqual(to_json["total results"], 2)
        self.assertEqual(to_json["total pages"], 1)
        self.assertEqual(to_json["cur page"], 1)
        self.assertEqual(to_json["prev page"], None)
        self.assertEqual(to_json["next page"], None)

    def test_rsvp_registered_user(self):
        """
        Test that API endpoint '/api/event/<eventId>/rsvp' reserves a guest
        """

        self.register_user()
        result = self.login_user()

        head = self.set_headers(result)

        res = self.create_event_helper(head, self.event_data)

        res = self.client().post(
                '/api/v2/event/daraja/rsvp',
                headers=head,
                data=json.dumps({"email":"user@test.com"})
                )
        self.assertEqual(res.status_code, 200)
        self.assertIn("Welcome user@test.com, your reservation for the event daraja has been approved", res.data)


    def test_rsvp_unregistered_user(self):
        """
        Test that API endpoint '/api/event/<eventId>/rsvp' reserves a guest without registration
        """

        self.register_user()

        result = self.login_user()
        head = self.set_headers(result)
        self.create_event_helper(head, self.event_data)

        res = self.client().post(
                '/api/v2/event/daraja/rsvp',
                headers=head,
                data=json.dumps({"email":"unregisteredUser@test.com"})
                )
        self.assertEqual(res.status_code, 200)
        self.assertIn("Welcome unregisteredUser@test.com, your reservation for the event daraja has been approved", res.data)
        self.assertIn("Your temporary password is 12345, please login and change it to a much safer password", res.data)

    def test_retrieve_reserved_guests(self):
        """
        Test that API endpoint '/api/event/<eventId>/rsvp' retrieves event guests
        """

        self.register_user()

        result = self.login_user()
        head = self.set_headers(result)
        self.create_event_helper(head, self.event_data)

        res = self.client().post(
                '/api/v2/event/daraja/rsvp',
                headers=head,
                data=json.dumps({"email":"user@test.com"})
                )
        self.assertEqual(res.status_code, 200)

        res = self.client().get(
                '/api/v2/event/daraja/rsvp',
                headers=head
                )
        self.assertEqual(res.status_code, 200)
        self.assertIn("Guests attending daraja", res.data)
        self.assertIn("user@test.com", res.data)
        self.assertIn("test", res.data)

    def test_error_handler_404(self):
        """
        Test how the Api handles a 404 error
        """

        self.register_user()
        result = self.login_user()

        head = self.set_headers(result)

        res = self.client().post(
                '/api/v2/groo',
                headers=head,
                data=json.dumps(self.event_data)
                )

        self.assertEqual(res.status_code, 404)
        self.assertIn("endpoint not found", res.data)

    def test_error_handler_405(self):
        """
        Test how the Api handles a 405 error
        """

        self.register_user()
        result = self.login_user()

        head = self.set_headers(result)

        res = self.client().delete(
                '/api/v2/events',
                headers=head,
                data=json.dumps(self.event_data)
                )

        self.assertEqual(res.status_code, 405)
        self.assertIn("method not allowed for the requested url", res.data)

    def test_error_handler_500(self):
        """
        Test how the Api handles a 500 error
        """

        return ""

    def test_render_api_as_root(self):
        """
        Tests if the api documentation is rendered as the root directory of the application
        """
        res = self.client().get('/')

        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.content_type, 'text/html; charset=utf-8')



    def tearDown(self):
        """teardown all initialized variables."""
        with self.app.app_context():
            # drop all tables
            db.session.remove()
            db.drop_all()

if __name__ == "__main__":
    unittest.main()
