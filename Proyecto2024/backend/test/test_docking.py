import unittest
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

        with self.app.session_transaction() as sess:
            sess["user_id"] = self.test_user.id

    def tearDown(self):
        # Limpiar la base de datos después de cada test
        db_session.query(Prediction).delete()
        db_session.query(User).delete()
        db_session.commit()

    def test_upload_and_submit_files(self):
        # Testear la subida de archivos
        with open("test_protein.pdb", "rb") as protein_file, open(
            "test_toxin.sdf", "rb"
        ) as toxin_file:
            response = self.app.post(
                "/upload", data={"file": protein_file, "type": "protein"}
            )
            self.assertEqual(response.status_code, 200)

            response = self.app.post(
                "/upload", data={"file": toxin_file, "type": "toxin"}
            )
            self.assertEqual(response.status_code, 200)

        # Testear la ruta de submit
        response = self.app.post(
            "/submit",
            data={
                "protein_file": open("test_protein.pdb", "rb"),
                "toxin_file": open("test_toxin.sdf", "rb"),
            },
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Files submitted and saved successfully", response.data)

    def test_docking_prediction(self):
        # Crear archivos de prueba y simular predicción de docking
        response = self.app.post(
            "/submit",
            data={
                "protein_file": open("test_protein.pdb", "rb"),
                "toxin_file": open("test_toxin.sdf", "rb"),
            },
        )
        self.assertEqual(response.status_code, 200)

        data = response.get_json()
        self.assertIn("result", data)
        self.assertIn("docking_score", data)


if __name__ == "__main__":
    unittest.main()
