import unittest

class TestSuperClass(unittest.TestCase):

    def test_return(self):
        return ""


class TestEndpoints(TestSuperClass):

    def test_register(self):
        """
        Test that API endpoint sends in registration details
        """


    def test_login(self):
        """
        Test that API endpoint sends in login details
        """
        return ""

    def test_password_reset(self):
        """
        Test that API endpoint sends in a password reset request
        """
        return ""

    def test_create_event(self):
        """
        Test that API endpoint sends in details to create an event
        """
        return ""

    def test_update_event(self):
        """
        Test that API endpoint has made an update request
        """
        return ""

    def test_delete_event(self):
        """
        Test that API endpoint has made a delete request
        """
        return ""

    def test_retrieve_event(self):
        """
        Test that API endpoint has made a request to retrieve an event
        """
        return ""

    def test_rsvp_event(self):
        """
        Test that API endpoint has made a request to rsvp an event
        """
        return ""

    def test_retrieve_all_guests(self):
        """
        Test that API endpoint has made a request to retrieve all events
        """
        return ""




if __name__ == "__main__":
    unittest.main()
