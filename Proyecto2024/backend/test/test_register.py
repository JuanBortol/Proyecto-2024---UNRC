import unittest
from app import app

class TestRegister(unittest.TestCase):

    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False  # Desactiva el CSRF para las pruebas
        self.client = app.test_client()

    def test_register_success(self):
        response = self.client.post('/register', data={
            'username': 'testuser',
            'password': 'testpassword',
            'confirm_password': 'testpassword'
        }, follow_redirects=True)
        
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Registration successful', response.data)

    def test_register_password_mismatch(self):
        response = self.client.post('/register', data={
            'username': 'testuser',
            'password': 'testpassword1',
            'confirm_password': 'testpassword2'
        }, follow_redirects=True)
        
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Passwords do not match', response.data)

    def test_register_missing_username(self):
        response = self.client.post('/register', data={
            'username': '',
            'password': 'testpassword',
            'confirm_password': 'testpassword'
        }, follow_redirects=True)
        
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Username is required', response.data)

    def test_register_existing_user(self):
        self.client.post('/register', data={
            'username': 'existinguser',
            'password': 'testpassword',
            'confirm_password': 'testpassword'
        }, follow_redirects=True)

        response = self.client.post('/register', data={
            'username': 'existinguser',
            'password': 'testpassword',
            'confirm_password': 'testpassword'
        }, follow_redirects=True)
        
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Username already exists', response.data)

if __name__ == '__main__':
    unittest.main()
