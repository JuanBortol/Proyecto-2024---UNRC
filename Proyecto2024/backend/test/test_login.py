import unittest

from flask import Flask
from app import app  # Cambia 'your_app' por el nombre real de tu archivo de aplicación

class LoginTestCase(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_login_success(self):
        response = self.app.post('/login', data={'username': 'testuser', 'password': 'testpass'})
        self.assertEqual(response.status_code, 200)

    def test_login_failure(self):
        response = self.app.post('/login', data={'username': 'wronguser', 'password': 'wrongpass'})
        self.assertNotEqual(response.status_code, 200)

if __name__ == '__main__':
    unittest.main()
