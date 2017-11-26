"""Flask API tests"""
import unittest
from models import users, events, logged_in, logged_out, updated_passwords, RSVP

class TestEndpoints(unittest.TestCase):
    """Runs tests on API endpoints"""

    def test_create_user(self):
        """
        Test that API endpoint ''/api/auth/register' creates a new user account
        """

        user = {"name":"Picado", "email":"picado@gmail.com"}
        users.append(user)
        self.assertEqual(len(users), 3)



    def test_login_user(self):
        """
        Test that API endpoint '/api/auth/login' adds login details
        """

        log = {'username':"Lannister"}
        logged_in.append(log)
        self.assertEqual(len(logged_in), 4)

    def test_logout_user(self):
        """
        Test that API endpoint '/api/auth/logout' adds in logut details
        """

        logout = {'username':"Jammie"}
        logged_out.append(logout)
        self.assertEqual(len(logged_in), 4)


    def test_reset_password(self):
        """
        Test that API endpoint '/api/auth/reset-password' adds password reset details
        """

        password_reset = {'password':'12345'}
        updated_passwords.append(password_reset)
        self.assertEqual(len(updated_passwords), 4)


    def test_create_event(self):
        """
        Test that API endpoint '/api/events' has created an event
        """
        event = {'title':'daughter', 'category':'music'}
        events.append(event)
        self.assertEqual(len(events), 3)

    def test_update_event(self):
        """
        Test that API endpoint '/api/events/<eventId>' has made an update request
        """
        event = [evnt for evnt in events if evnt["title"] == "daughter"]
        event[0]["title"] = "Mahalo"
        self.assertEqual(event[0]["title"], "Mahalo")

    def test_delete_event(self):
        """
        Test that API endpoint '/api/events/<eventId>' has deleted an event
        """

        event = [event for event in events if event["title"] == "Flamenco"]
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

        reserved_guests = {'name':'Jason'}
        RSVP.append(reserved_guests)

        self.assertEqual(len(RSVP), 4)

if __name__ == "__main__":
    unittest.main()
