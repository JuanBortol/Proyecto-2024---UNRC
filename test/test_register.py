import unittest
from flask import Flask
from flask.testing import FlaskClient
from app import app  # Asegúrate de que 'app' esté definido en el archivo principal de Flask

class RegisterTestCase(unittest.TestCase):
    def setUp(self):
        # Crear una aplicación de prueba
        self.app = app.test_client()
        self.app.testing = True

    def test_register_page_loads(self):
        # Probar si la página de registro carga correctamente
        response = self.app.get('/register')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Register', response.data)  # Verifica que la página tenga la palabra 'Register'

    def test_register_success(self):
        # Probar si el registro es exitoso con datos correctos
        response = self.app.post('/register', data=dict(
            username='newuser', password='newpassword', confirm_password='newpassword'
        ), follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Registration successful', response.data)  # Asume que hay un mensaje de éxito

    def test_register_password_mismatch(self):
        # Probar si el registro falla cuando las contraseñas no coinciden
        response = self.app.post('/register', data=dict(
            username='newuser', password='newpassword', confirm_password='wrongpassword'
        ), follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Passwords must match', response.data)  # Asume que hay un mensaje de error

    def test_register_existing_user(self):
        # Probar si el registro falla cuando el usuario ya existe
        response = self.app.post('/register', data=dict(
            username='existinguser', password='password', confirm_password='password'
        ), follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'User already exists', response.data)  # Asume que hay un mensaje de error

if __name__ == '__main__':
    unittest.main()
