# I use unittest to run tests and get things I need from my main a
import unittest
from app import app
from app import user_exists


# Prepares app for testing - it turns on test mode and sets up test user details
class StrokesHospitalApp(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        self.app = app.test_client()
        self.username = "chis"
        self.email = "chis@gmail.com"

        # If home page opens

    def test_home_page(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)

        # If login page opens

    def test_login(self):
        response = self.app.get('/login')
        self.assertEqual(response.status_code, 200)

        # If register page opens

    def test_register_page(self):
        response = self.app.get('/register_page')
        self.assertEqual(response.status_code, 200)

        # If app blocks access to patient list when not logged in

    def test_patient_list_redirect_when_not_logged_in(self):
        response = self.app.get('/patients_list')
        self.assertEqual(response.status_code, 302)

        # If app can find existing users in database

    def test_registration(self):
        response = self.app.get('/register_page')
        self.assertEqual(response.status_code, 200)

        # If login endpoint responds correctly

    def test_login(self):
        response = self.app.get('/login')
        self.assertEqual(response.status_code, 200)

        # Tests if user registration works

    def test_user_exists(self):
        self.app.post('/user_register', data={
            'name': self.username,
            'email': self.email,
            'password': 'test123'
        })
        self.assertTrue(user_exists(self.username, self.email))

        # If app correctly says when user doesn't exist

    def test_user_not_exists(self):
        self.assertFalse(user_exists('NonExistenUser', 'nonexistent@example.com'))


# This runs all my tests when I run this file directly
if __name__ == '__main__':
    unittest.main()

