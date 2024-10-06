import React, { useState, useEffect, useContext } from 'react';
import Navbar from '../components/Navbar';
import Loading from '../components/Loading';
import httpClient from '../utils/httpClient';
import styles from '../styles/History.module.css';
import { AppContext } from '../components/AppContext';

export default function History() {
  const { darkMode } = useContext(AppContext);
  const [loading, setLoading] = useState(true);
  const [predictions, setPredictions] = useState([]);
  const [page, setPage] = useState(1);
  const itemsPerPage = 5;

  useEffect(() => {
    httpClient.get('http://localhost:5000/predictions')
      .then((res) => {
        setPredictions(res.data.reverse());
        setLoading(false)
      })
      .catch((error) => {
        console.error('Error fetching predictions:', error);
      });
  }, []);

  const startIndex = (page - 1) * itemsPerPage;
  const selectedPredictions = predictions.slice(startIndex, startIndex + itemsPerPage);

  if (loading) return <Loading />;

  return (
    <>
      <div className={`flex items-center justify-center text-white min-h-screen px-4
      ${darkMode ? 'bg-black' : styles.bgGreenGradient}`}>
        <Navbar />
        <div className='container min-h-full my-24 space-y-24 md:space-y-48 mx-4'>
          <h1 className="text-center text-7xl font-extrabold">historial</h1>
          <div>
            <div className="flex justify-between w-full font-extralight text-lg text-white py-2">
              <div className="buttons space-x-8">
                <button
                  onClick={() => setPage(page - 1)}
                  disabled={page === 1}
                >
                  anterior
                </button>
                <button
                  onClick={() => setPage(page + 1)}
                  disabled={page * itemsPerPage >= predictions.length}
                >
                  siguiente
                </button>
              </div>
              <p>página {page} de {(predictions.length > 1) ? Math.ceil(predictions.length / itemsPerPage) : 1}</p>
            </div>
            <table className="w-full text-center text-white rounded-md overflow-hidden">
            <thead className="bg-opacity-20 bg-white">
                <tr className="text-lg">
                  <th className="px-4 py-2 font-light">fecha</th>
                  <th className="px-4 py-2 font-light chain-col">proteina</th>
                  <th className="px-4 py-2 font-light model-col">toxina</th>
                  <th className="px-4 py-2 font-light">docking</th>
                  <th className="px-4 py-2 font-light">docking score</th>
                </tr>
              </thead>
              <tbody>
                {selectedPredictions.length > 0 ? (
                  selectedPredictions.map((prediction, index) => (
                    <tr key={index} className="bg-opacity-15 bg-white">
                      <td className="px-4 py-4">{prediction.date}</td>
                      <td className={`px-4 py-4 ${styles.proteinCol}`}>{prediction.protein_filename}</td>
                      <td className={`px-4 py-4 ${styles.toxinCol}`}>{prediction.toxin_filename}</td>
                      <td className="px-4 py-4">{prediction.result ? 'Sí' : 'No'}</td>
                      <td className="px-4 py-4 font-extrabold">{prediction.docking_score ? prediction.docking_score : '-'}</td>
                    </tr>
                  ))
                ) : (
                  <tr>
                    <td colSpan="4" className="px-4 py-8 font-extralight">no se encuentran registros</td>
                  </tr>
                )}
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </>
  );
}