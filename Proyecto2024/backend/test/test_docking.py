import unittest
from io import BytesIO
from flask import session
from app import app, db_session, Prediction, User


class TestDockingPredictions(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

        # Crear un usuario de prueba
        self.test_user = User(username="testuser", password="password")
        db_session.add(self.test_user)
        db_session.commit()

        # Iniciar sesión en el contexto de la prueba
        with self.app.session_transaction() as sess:
            sess["user_id"] = self.test_user.id

    def tearDown(self):
        # Limpiar la base de datos después de cada test
        db_session.query(Prediction).delete()
        db_session.query(User).delete()
        db_session.commit()

    def test_upload_and_submit_files(self):
        # Testear la subida de archivos con datos de ejemplo en memoria
        protein_data = BytesIO(b"Test protein data")
        toxin_data = BytesIO(b"Test toxin data")

        response = self.app.post(
            "/upload",
            data={"file": (protein_data, "test_protein.pdb"), "type": "protein"},
        )
        self.assertEqual(response.status_code, 200)

        response = self.app.post(
            "/upload", data={"file": (toxin_data, "test_toxin.sdf"), "type": "toxin"}
        )
        self.assertEqual(response.status_code, 200)

        # Testear la ruta de submit
        response = self.app.post(
            "/submit",
            data={
                "protein_file": (BytesIO(b"Test protein data"), "test_protein.pdb"),
                "toxin_file": (BytesIO(b"Test toxin data"), "test_toxin.sdf"),
            },
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Files submitted and saved successfully", response.data)

    def test_docking_prediction(self):
        # Crear archivos de prueba y simular predicción de docking
        response = self.app.post(
            "/submit",
            data={
                "protein_file": (BytesIO(b"Test protein data"), "test_protein.pdb"),
                "toxin_file": (BytesIO(b"Test toxin data"), "test_toxin.sdf"),
            },
        )
        self.assertEqual(response.status_code, 200)

        # Verificar los resultados de la predicción
        data = response.get_json()
        self.assertIn("result", data)
        self.assertIn("docking_score", data)


if __name__ == "__main__":
    unittest.main()
