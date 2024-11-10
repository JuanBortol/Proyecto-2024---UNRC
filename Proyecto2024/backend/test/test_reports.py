import unittest
from app import app, db_session, Report, User

class TestReportHandling(unittest.TestCase):
    
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

        # Crear un usuario de prueba
        self.test_user = User(username='testuser', password='password')
        db_session.add(self.test_user)
        db_session.commit()

        with self.app.session_transaction() as sess:
            sess['user_id'] = self.test_user.id

    def tearDown(self):
        # Limpiar la base de datos después de cada test
        db_session.query(Report).delete()
        db_session.query(User).delete()
        db_session.commit()

    def test_submit_report(self):
        # Testear la subida de informe
        with open('test_protein.pdb', 'rb') as protein_file, open('test_toxin.sdf', 'rb') as toxin_file, open('test_report.pdf', 'rb') as pdf_file:
            response = self.app.post('/submit_report', data={
                'protein_file': protein_file,
                'toxin_file': toxin_file,
                'pdf_file': pdf_file,
                'reason': 'Testing report submission'
            })
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'Report successfully submitted', response.data)

    def test_submit_report_missing_data(self):
        # Intentar enviar un informe sin todos los datos requeridos
        with open('test_protein.pdb', 'rb') as protein_file:
            response = self.app.post('/submit_report', data={
                'protein_file': protein_file,
                'reason': 'Missing toxin file'
            })
            self.assertEqual(response.status_code, 400)
            self.assertIn(b'protein file and reason are required', response.data)

if __name__ == '__main__':
    unittest.main()
