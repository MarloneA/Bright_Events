import unittest
import os
import json
from app import create_app, db
from app.models import User, Event

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
            'description':'a small intimate setting for singers, musicians and poetry collaborations'
        }

        # binds the app to the current context
        with self.app.app_context():
            # create all tables
            db.create_all()

    def test_create_event(self):
        """
        Test that API endpoint '/api/events' has created an event
        """

        res = self.client().post(
                '/api/v2/events',
                data=json.dumps(self.event_data)
                )

        self.assertEqual(res.status_code, 201)


    def test_retrieve_events(self):
        """
        Test that APi endpoint retrieves all events
        """

        res = self.client().post('api/v2/events', data=json.dumps(self.event_data))
        self.assertEqual(res.status_code, 201)

        res = self.client().get('/api/v2/events')
        self.assertEqual(res.status_code, 200)


    def test_update_event(self):
        """
        Test that API endpoint '/api/events/<eventId>' has made an update request
        """

        resU = self.client().post(
            '/api/v2/events',
            data=json.dumps({
            	"title":"it",
            	"location":"derry",
            	"category":"horror",
            	"description":"Come see pennywise the clown in action"
                }))
        self.assertEqual(resU.status_code, 201)

        resU = self.client().put(
            '/api/v2/events/it',
            data=json.dumps({
                "title":"it",
            	"location":"derry",
            	"category":"horror",
                "description": "Billy Denbrough beats the devil"
            }))
        self.assertEqual(resU.status_code, 200)

    def test_delete_event(self):
        """
        Test that API endpoint '/api/events/<eventId>' has deleted an event
        """

        rv = self.client().post(
                'api/v2/events',
                data=json.dumps({
                "title":"it",
                "location":"derry",
                "category":"horror",
                "description":"Come see pennywise the clown in action"
                }))
        self.assertEqual(rv.status_code, 201)

        res = self.client().delete('api/v2/events/it')
        self.assertEqual(res.status_code, 200)

        result = self.client().get('api/v2/events/it')

        self.assertEqual(result.status_code, 400)
        self.assertIn("event not found!", result.data)

    def test_search_for_event(self):
        """
        Test that API endpoint '/api/events/<searchQuery>' retrieves the requested event
        """

        res = self.client().post('api/v2/events', data=json.dumps(self.event_data))
        self.assertEqual(res.status_code, 201)

        res = self.client().get('/api/v2/events/daraja')
        self.assertEqual(res.status_code, 200)


    def test_filter_event_by_category(self):
        """
        Test that API endpoint '/api/v2/events/category/<category>' filters events by a category
        """
        return ""

    def test_filter_event_by_location(self):
        """
        Test that API endpoint '/api/v2/events/location/<location>' filters events by location
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

    def test_render_api_as_root(self):
        """
        Tests if documentation is rendered as the root of the application
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