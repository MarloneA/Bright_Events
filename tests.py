import unittest

class  TestApp(unittest.TestCase):
    def test_app_exists(self):
        """
        Test wether the app exists
        """
        self.assertFalse(current_app is None)

    

if __name__ == "__main__":
    unittest.main()
