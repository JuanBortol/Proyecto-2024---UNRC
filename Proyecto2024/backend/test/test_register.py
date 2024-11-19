import unittest
from app import app
from database import db_session
from models.user import User


class TestRegister(unittest.TestCase):

    def setUp(self):
        app.config["TESTING"] = True
        app.config["WTF_CSRF_ENABLED"] = False  # Desactiva el CSRF para las pruebas
        self.client = app.test_client()

    def tearDown(self):
        # Limpia los usuarios de prueba después de cada test
        db_session.query(User).filter(
            User.username.in_(["testuser", "existinguser"])
        ).delete()
        db_session.commit()

    def test_register_success(self):
        response = self.client.post(
            "/register",
            json={
                "username": "testuser",
                "password": "testpassword",
                "confirm_password": "testpassword",
            },
            follow_redirects=True,
        )
        response_json = response.get_json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_json["message"], "Usuario registrado con éxito")

    def test_register_password_mismatch(self):
        response = self.client.post(
            "/register",
            json={
                "username": "testuser",
                "password": "testpassword1",
                "confirm_password": "testpassword2",
            },
            follow_redirects=True,
        )
        response_json = response.get_json()
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response_json["message"], "Las contraseñas no coinciden")

    def test_register_missing_username(self):
        response = self.client.post(
            "/register",
            json={
                "username": "",
                "password": "testpassword",
                "confirm_password": "testpassword",
            },
            follow_redirects=True,
        )
        response_json = response.get_json()
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response_json["message"], "Todos los campos son obligatorios")

    def test_register_existing_user(self):
        # Primero, registra al usuario para que luego falle por duplicado
        self.client.post(
            "/register",
            json={
                "username": "existinguser",
                "password": "testpassword",
                "confirm_password": "testpassword",
            },
            follow_redirects=True,
        )

        # Intenta registrar el mismo usuario nuevamente
        response = self.client.post(
            "/register",
            json={
                "username": "existinguser",
                "password": "testpassword",
                "confirm_password": "testpassword",
            },
            follow_redirects=True,
        )
        response_json = response.get_json()
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response_json["message"], "El usuario ya existe")


if __name__ == "__main__":
    unittest.main()
