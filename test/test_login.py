import unittest
from flask import Flask
from flask.testing import FlaskClient
from app import app  # Asegúrate de que 'app' esté definido en el archivo principal de Flask

class LoginTestCase(unittest.TestCase):
    def setUp(self):
        # Crear una aplicación de prueba
        self.app = app.test_client()
        self.app.testing = True

    def test_login_page_loads(self):
        # Probar si la página de login carga correctamente
        response = self.app.get('/login')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Login', response.data)  # Verifica que la página tenga la palabra 'Login'

    def test_login_success(self):
        # Probar si el login es exitoso con las credenciales correctas
        response = self.app.post('/login', data=dict(
            username='testuser', password='testpassword'
        ), follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Login successful', response.data)  # Asume que hay un mensaje de éxito

    def test_login_failure(self):
        # Probar si el login falla con credenciales incorrectas
        response = self.app.post('/login', data=dict(
            username='wronguser', password='wrongpassword'
        ), follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Invalid credentials', response.data)  # Asume que hay un mensaje de error

if __name__ == '__main__':
    unittest.main()
