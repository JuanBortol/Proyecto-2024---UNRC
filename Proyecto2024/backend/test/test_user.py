import unittest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from models.user import User
from models.report import Report
from database import Base


class TestUserModel(unittest.TestCase):

    # Crea un motor en memoria para la base de datos de pruebas
    @classmethod
    def setUpClass(cls):
        cls.engine = create_engine("sqlite:///:memory:")
        Base.metadata.create_all(cls.engine)
        Session = sessionmaker(bind=cls.engine)
        cls.session = Session()

    # Cierra la sesion y eliminar la base de datos
    @classmethod
    def tearDownClass(cls):
        cls.session.close()

    def setUp(self):
        self.session.rollback()
        self.session.query(Report).delete()
        self.session.query(User).delete()
        self.session.commit()

    # Test para crear un usuario
    def test_create_user(self):
        user = User(username="test_user", password="test_password")
        self.session.add(user)
        self.session.commit()

        saved_user = self.session.query(User).filter_by(username="test_user").first()
        self.assertIsNotNone(saved_user)
        self.assertEqual(saved_user.username, "test_user")
        self.assertEqual(saved_user.password, "test_password")

    def test_unique_username(self):
        user1 = User(username="unique_user", password="password1")
        user2 = User(username="unique_user", password="password2")

        self.session.add(user1)
        self.session.commit()

        self.session.add(user2)
        with self.assertRaises(Exception):
            try:
                self.session.commit()  
            finally:
                self.session.rollback()  


def test_user_report_relationship(self):
    # Crear usuario
    user = User(username="report_user", password="password123")
    self.session.add(user)
    self.session.commit()

    # Crear reportes asociados al usuario
    report1 = Report(protein="Protein A", toxin="Toxin X", reason="Test Reason 1", user_id=user.id)
    report2 = Report(protein="Protein B", toxin="Toxin Y", reason="Test Reason 2", user_id=user.id)
    self.session.add_all([report1, report2])
    self.session.commit()

    # Verificar que los reportes están asociados al usuario correcto
    saved_user = self.session.query(User).filter_by(username="report_user").first()
    self.assertEqual(len(saved_user.reports), 2)
    self.assertEqual(saved_user.reports[0].protein, "Protein A")
    self.assertEqual(saved_user.reports[1].protein, "Protein B")

    # Verificar que cada reporte puede acceder a su usuario
    saved_report1 = self.session.query(Report).filter_by(protein="Protein A").first()
    self.assertEqual(saved_report1.user.username, "report_user")

    saved_report2 = self.session.query(Report).filter_by(protein="Protein B").first()
    self.assertEqual(saved_report2.user.username, "report_user")



if __name__ == "__main__":
    unittest.main()