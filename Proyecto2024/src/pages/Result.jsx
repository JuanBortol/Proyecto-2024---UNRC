import React, { useState, useContext } from 'react';
import Navbar from '../components/Navbar';
import axios from 'axios';
import { AppContext } from '../components/AppContext';

export default function Report() {
  const { darkMode } = useContext(AppContext);
  const [dockingResult, setDockingResult] = useState('');
  const [filesDocked, setFilesDocked] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const runDocking = async () => {
    setLoading(true);
    setError('');

    const formData = new FormData();
    formData.append('protein', "../uploads/trogii.pdb" ); // Usa el archivo real, no la ruta
    formData.append('ligand', "../uploads/AFB1_ligand_1.pdb");   // Usa el archivo real, no la ruta

    try {
      const response = await axios.post('http://localhost:5000/run_docking', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });

      if (response.data.result) {
        setDockingResult(response.data.result);
      }
      if (response.data.files_docked) {
        setFilesDocked(response.data.files_docked);
      }
      if (response.data.error) {
        setError(response.data.error);
      }
    } catch (err) {
      setError('Error al realizar la simulación de docking');
    } finally {
      setLoading(false);
    }
  };

  return (
      <div
          className={`flex flex-col items-center justify-center text-white min-h-screen space-y-32 
      ${darkMode ? 'bg-black' : 'bg-gradient-to-b from-blue-500 to-green-500'}`}
      >
        <Navbar />
        <div className='container space-y-24'>
          <div className="flex flex-col items-center w-full space-y-12 px-8">
            <h1 className="text-center text-7xl font-extrabold">Resultado de Docking</h1>

            {loading && <p>Cargando...</p>}
            {error && <p className="text-red-500">{error}</p>}
            {dockingResult && (
                <div className="bg-gray-800 p-4 rounded-lg shadow-lg text-white">
                  <h2 className="text-3xl font-bold mb-4">Resultado:</h2>
                  <p className="text-xl">{dockingResult}</p>
                </div>
            )}

            <button
                onClick={runDocking}
                className="mt-10 px-6 py-3 bg-green-600 text-white rounded-lg hover:bg-green-800"
                disabled={loading}
            >
              Ejecutar Docking
            </button>

            {filesDocked.length > 0 && (
                <div className="mt-12">
                  <h3 className="text-2xl font-semibold mb-4">Proteínas que hicieron docking:</h3>
                  <ul className="list-disc list-inside">
                    {filesDocked.map((file, index) => (
                        <li key={index}>{file}</li>
                    ))}
                  </ul>
                </div>
            )}
          </div>
        </div>
      </div>
  );
}
