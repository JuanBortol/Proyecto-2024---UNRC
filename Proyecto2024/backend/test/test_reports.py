import unittest
from io import BytesIO
from app import app, db_session, Report, User


class TestReportHandling(unittest.TestCase):

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
        db_session.query(Report).delete()
        db_session.query(User).delete()
        db_session.commit()

    def test_submit_report(self):
        # Simular subida de informe con datos en memoria
        protein_data = BytesIO(b"Test protein data")
        toxin_data = BytesIO(b"Test toxin data")
        report_data = BytesIO(b"Test PDF report data")

        response = self.app.post(
            "/submit_report",
            data={
                "protein_file": (protein_data, "test_protein.pdb"),
                "toxin_file": (toxin_data, "test_toxin.sdf"),
                "pdf_file": (report_data, "test_report.pdf"),
                "reason": "Testing report submission",
            },
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Report successfully submitted", response.data)

    def test_submit_report_missing_data(self):
        # Intentar enviar un informe sin todos los datos requeridos
        protein_data = BytesIO(b"Test protein data")

        response = self.app.post(
            "/submit_report",
            data={
                "protein_file": (protein_data, "test_protein.pdb"),
                "reason": "Missing toxin file",
            },
        )
        self.assertEqual(response.status_code, 400)
        self.assertIn(b"protein file and reason are required", response.data)


if __name__ == "__main__":
    unittest.main()
