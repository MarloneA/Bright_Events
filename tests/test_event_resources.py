import json
from tests.base import BaseTestCase
from app import version

class TestEvent(BaseTestCase):
    """
    This Class covers tests centered around CRUD operations of the API
    """

    def test_create_event(self):
        """
        Test that API endpoint '/api/events' has created an event
        """

        self.register_helper(self.user_data)
        result = self.login_user()

        print(result)

        head = self.set_headers(result)
        res = self.create_event_helper(head, self.event_data)

        self.assertEqual(res.status_code, 201)
        self.assertIn("new event has been created", res.data.decode())


    def test_create_event_with_empty_title(self):
        """
        Tests users ahould not be able to create titles with empty spaces
        """

        self.register_helper(self.user_data)
        result = self.login_user()

        head = self.set_headers(result)
        res = self.create_event_helper(head, self.empty_title)

        self.assertEqual(res.status_code, 400)
        self.assertIn("Please provide a valid title", res.data.decode())

    def test_create_event_with_title_as_integer(self):
        """
        Test users should not be able to supply integers as titles
        """

        self.register_helper(self.user_data)
        result = self.login_user()

        head = self.set_headers(result)
        res = self.create_event_helper(head, self.int_title)

        self.assertEqual(res.status_code, 400)
        self.assertIn("title cannot be an integer", res.data.decode())

    def test_retrieve_events(self):
        """
        Test that APi endpoint retrieves all events recorded in the db
        """

        self.register_helper(self.user_data)
        result = self.login_user()

        head = self.set_headers(result)

        self.create_event_helper(head, self.event_data)
        self.event_data["title"]="daraj"
        self.create_event_helper(head, self.event_data)
        self.event_data["title"]="dara"
        self.create_event_helper(head, self.event_data)
        self.event_data["title"]="dar"
        self.create_event_helper(head, self.event_data)

        res = self.client().get(version+'/events/10/1', headers=head)

        to_json =  json.loads(res.data.decode())

        self.assertEqual(res.status_code, 200)
        self.assertEqual(to_json["total results"], 4)
        self.assertEqual(to_json["cur page"], 1)
        self.assertEqual(to_json["total pages"], 1)


    def test_update_event(self):
        """
        Test that API endpoint '/api/events/<eventId>' has made an update request
        """

        self.register_helper(self.user_data)
        result = self.login_user()

        head = self.set_headers(result)
        self.create_event_helper(head, self.event_data)

        data=json.dumps(self.update_data)
        resU = self.client().put(version+'/events/1', headers=head, data=data)

        self.assertEqual(resU.status_code, 200)
        self.assertIn("The event has been updated!", resU.data.decode())


    def test_delete_event(self):
        """
        Test that API endpoint '/api/events/<eventId>' has deleted an event
        """

        self.register_helper(self.user_data)
        result = self.login_user()

        head = self.set_headers(result)
        self.create_event_helper(head, self.event_data)

        res = self.client().delete('api/v2/events/1', headers=head)
        self.assertEqual(res.status_code, 200)

        result = self.client().get('api/v2/events/it/1/1',headers=head)

        self.assertEqual(result.status_code, 400)
        self.assertIn("event not found!", result.data.decode())

    def test_search_for_event(self):
        """
        Test that API endpoint '/api/events/<searchQuery>/<int:results/<int:page_num>' retrieves the requested event
        """

        self.register_helper(self.user_data)
        result = self.login_user()

        head = self.set_headers(result)
        self.create_event_helper(head, self.event_data)

        res = self.client().get(version+'/events/daraja/5/1')
        to_json =  json.loads(res.data.decode())

        self.assertEqual(res.status_code, 200)
        self.assertEqual(len(to_json["Search_Results"]), 1)
        self.assertEqual(to_json["total results"], 1)
        self.assertEqual(to_json["total pages"], 1)
        self.assertEqual(to_json["cur page"], 1)
        self.assertEqual(to_json["prev page"], None)
        self.assertEqual(to_json["next page"], None)


    def test_filter_event_by_category(self):
        """
        Test that API endpoint version+'/events/category/<category>' filters events by a category
        """
        self.register_helper(self.user_data)
        result = self.login_user()

        head = self.set_headers(result)

        self.create_event_helper(head, self.filter_data[0])
        self.create_event_helper(head, self.filter_data[1])
        self.create_event_helper(head, self.filter_data[2])

        result = self.client().get(version+'/events/category/music/5/1')
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
        Test that API endpoint version+'/events/location/<location>' filters events by location
        """

        self.register_helper(self.user_data)
        result = self.login_user()

        head = self.set_headers(result)

        self.create_event_helper(head, self.filter_data[0])
        self.create_event_helper(head, self.filter_data[1])
        self.create_event_helper(head, self.filter_data[2])

        result = self.client().get(version+'/events/location/derry/5/1')
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

        self.register_helper(self.user_data)
        result = self.login_user()

        head = self.set_headers(result)
        self.create_event_helper(head, self.event_data)

        res = self.reserve_event_helper(head, "user@test.com")

        self.assertEqual(res.status_code, 200)
        self.assertIn("Welcome user, your reservation for the event daraja has been approved", res.data.decode())


    def test_rsvp_unregistered_user(self):
        """
        Test that API endpoint '/api/event/<eventId>/rsvp' reserves a guest without registration
        """

        self.register_helper(self.user_data)

        result = self.login_user()
        head = self.set_headers(result)
        self.create_event_helper(head, self.event_data)

        res = self.reserve_event_helper(head, "unregistered.user@test.com")

        self.assertEqual(res.status_code, 200)
        self.assertIn("Welcome unregistered.user, your reservation for the event daraja has been approved", res.data.decode())
        self.assertIn("Your temporary password is, use it to login and set a safer password", res.data.decode())

    def test_retrieve_reserved_guests(self):
        """
        Test that API endpoint '/api/event/<eventId>/rsvp' retrieves event guests
        """

        self.register_helper(self.user_data)
        result = self.login_user()
        head = self.set_headers(result)

        self.create_event_helper(head, self.event_data)
        self.reserve_event_helper(head, "user@test.com")


        res = self.client().get(
                version+'/event/1/rsvp',
                headers=head
                )
        self.assertEqual(res.status_code, 200)
        self.assertIn("Guests attending daraja", res.data.decode())
        self.assertIn("user@test.com", res.data.decode())
        self.assertIn("test", res.data.decode())

    def test_error_handler_404(self):
        """
        Test how the Api handles a 404 error
        """

        self.register_helper(self.user_data)
        result = self.login_user()

        head = self.set_headers(result)

        res = self.client().post(
                version+'/groo',
                headers=head,
                data=json.dumps(self.event_data)
                )

        self.assertEqual(res.status_code, 404)
        self.assertIn("resource not found", res.data.decode())

    def test_error_handler_405(self):
        """
        Test how the Api handles a 405 error
        """

        self.register_helper(self.user_data)
        result = self.login_user()

        head = self.set_headers(result)

        res = self.client().delete(
                version+'/events',
                headers=head,
                data=json.dumps(self.event_data)
                )

        self.assertEqual(res.status_code, 405)
        self.assertIn("method not allowed for the requested resource", res.data.decode())

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


if __name__ == "__main__":
    unittest.main()
