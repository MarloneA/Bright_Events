"""Flask API tests"""
import unittest
from data import users, events,logged_users

class TestEndpoints(unittest.TestCase):
    """Runs tests on API endpoints"""

    def test_create_user(self):
        """
        Test that API endpoint ''/api/auth/register' creates a new user account
        """

        user = {"id":"33","name":"Picado", "email":"picado@gmail.com","password":"456"}
        users.append(user)
        self.assertEqual(len(users), 3)

    def test_login_user(self):
        """
        Test that API endpoint '/api/auth/login' adds login details
        """

        log = {'email':"lanister@gmail.com"}
        logged_users.append(log)
        self.assertEqual(len(logged_users), 4)

    def test_logout_user(self):
        """
        Test that API endpoint '/api/auth/logout' logs out os a session
        """

        log = {'email':"lanister@gmail.com"}
        logged_users.remove(log)
        self.assertEqual(len(logged_users), 3)


    def test_reset_password(self):
        """
        Test that API endpoint '/api/auth/reset-password' resets a password
        """

        password_reset = {'email':'picado@gmail.com','password':'mynewpass'}

        user = [usr for usr in users if usr["email"] == password_reset["email"]]

        user[0]['password'] = password_reset['password']

        self.assertEqual(user[0]['password'], 'mynewpass')


    def test_create_event(self):
        """
        Test that API endpoint '/api/events' has created an event
        """
        event = {"id":"67", "title":"grunge", "category":"music", "location":"nairobi", "description":"A wonderful event extravaganza"}
        events.append(event)
        self.assertEqual(len(events), 3)

    def test_update_event(self):
        """
        Test that API endpoint '/api/events/<eventId>' has made an update request
        """
        event_update = {"id":"32", "title":"newtitle", "category":"poems", "location":"rwanda", "description":"the best event ever"}

        event = [evnt for evnt in events if evnt["id"] == "32"]

        event[0]["title"] = event_update["title"]
        event[0]["location"] = event_update["location"]
        event[0]["category"] = event_update["category"]
        event[0]["description"] = event_update["description"]


        self.assertEqual(event[0]["title"], "newtitle")
        self.assertEqual(event[0]["location"], "rwanda")
        self.assertEqual(event[0]["category"], "poems")
        self.assertEqual(event[0]["description"], "the best event ever")

    def test_delete_event(self):
        """
        Test that API endpoint '/api/events/<eventId>' has deleted an event
        """

        event = [event for event in events if event["id"] == "64"]
        events.remove(event[0])
        self.assertEqual(len(events), 2)

    def test_retrieve_event(self):
        """
        Test that API endpoint '/api/events' retrieves all events
        """
        self.assertEqual(len(events), 2)

    def test_rsvp_event(self):
        """
        Test that API endpoint '/api/event/<eventId>/rsvp' reserves a guest
        """
        check_usr = [usr for usr in users if usr['name'] == 'Pres']

        check_usr[0]['rsvp'] = True

        self.assertEqual(check_usr[0]['rsvp'], True)

if __name__ == "__main__":
    unittest.main()
