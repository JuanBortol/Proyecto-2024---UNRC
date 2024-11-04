import unittest
from app import app, db_session, User, Prediction

class TestQueryEndpoints(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

        # Crear un usuario y predicciones de prueba
        self.test_user = User(username='testuser', password='password')
        db_session.add(self.test_user)
        db_session.commit()

        # Asociar predicciones de prueba con el usuario
        self.prediction1 = Prediction(user_id=self.test_user.id, result="Prediction 1", score=85)
        self.prediction2 = Prediction(user_id=self.test_user.id, result="Prediction 2", score=75)
        db_session.add(self.prediction1)
        db_session.add(self.prediction2)
        db_session.commit()

    def tearDown(self):
        # Limpiar la base de datos después de cada test
        db_session.query(Prediction).delete()
        db_session.query(User).delete()
        db_session.commit()

    def test_query_user_info(self):
        # Test para consultar información del usuario
        response = self.app.get(f'/user/{self.test_user.id}')
        self.assertEqual(response.status_code, 200)
        
        # Verificar si los datos de usuario son correctos
        data = response.get_json()
        self.assertEqual(data['username'], 'testuser')
        self.assertIn('predictions', data)  # Verificar que se incluyan predicciones
        self.assertEqual(len(data['predictions']), 2)

    def test_query_prediction_details(self):
        # Test para consultar detalles de una predicción
        response = self.app.get(f'/prediction/{self.prediction1.id}')
        self.assertEqual(response.status_code, 200)
        
        # Verificar si los datos de predicción son correctos
        data = response.get_json()
        self.assertEqual(data['result'], 'Prediction 1')
        self.assertEqual(data['score'], 85)

    def test_query_nonexistent_user(self):
        # Test para verificar la respuesta a una consulta de usuario inexistente
        response = self.app.get('/user/999')
        self.assertEqual(response.status_code, 404)
        self.assertIn(b'User not found', response.data)

    def test_query_nonexistent_prediction(self):
        # Test para verificar la respuesta a una consulta de predicción inexistente
        response = self.app.get('/prediction/999')
        self.assertEqual(response.status_code, 404)
        self.assertIn(b'Prediction not found', response.data)

if __name__ == '__main__':
    unittest.main()
