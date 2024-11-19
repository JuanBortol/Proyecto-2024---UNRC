import unittest
import os
from flask import Flask
from io import BytesIO
from your_flask_app import (
    app,
    db_session,
)  # Asegúrate de importar la aplicación correctamente


class ProteinUploadTestCase(unittest.TestCase):

    def setUp(self):
        app.config["TESTING"] = True
        app.config["UPLOAD_FOLDER"] = "test_uploads/"
        self.client = app.test_client()

        if not os.path.exists(app.config["UPLOAD_FOLDER"]):
            os.makedirs(app.config["UPLOAD_FOLDER"])

    def tearDown(self):
        # Limpiar archivos subidos
        if os.path.exists(app.config["UPLOAD_FOLDER"]):
            for file in os.listdir(app.config["UPLOAD_FOLDER"]):
                file_path = os.path.join(app.config["UPLOAD_FOLDER"], file)
                os.remove(file_path)

    def test_upload_protein(self):
        # Simulamos el archivo a subir
        data = {
            "file": (BytesIO(b"Dummy protein data"), "protein.pdb"),
            "type": "protein",
        }

        response = self.client.post(
            "/upload", data=data, content_type="multipart/form-data"
        )

        # Comprobamos si la respuesta fue exitosa
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"File uploaded successfully", response.data)

        # Verificar si el archivo fue guardado correctamente en el servidor
        uploaded_file_path = os.path.join(app.config["UPLOAD_FOLDER"], "protein.pdb")
        self.assertTrue(os.path.exists(uploaded_file_path))


if __name__ == "__main__":
    unittest.main()
