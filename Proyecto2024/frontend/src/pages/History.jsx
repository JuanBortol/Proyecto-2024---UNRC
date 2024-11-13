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
    httpClient.get('/predictions')
      .then((res) => {
        setPredictions(res.data.reverse());
        setLoading(false);
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
        <div className="container min-h-full my-24 space-y-24 md:space-y-48 mx-4">
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
            <div className="overflow-x-auto">
              <table className="w-full text-center text-white rounded-md overflow-hidden hidden md:table">
                <thead className="bg-opacity-20 bg-white">
                  <tr className="text-lg">
                    <th className="px-4 py-2 font-light">fecha</th>
                    <th className="px-4 py-2 font-light">proteina</th>
                    <th className="px-4 py-2 font-light">toxina</th>
                    <th className="px-4 py-2 font-light">docking</th>
                    <th className="px-4 py-2 font-light">docking score</th>
                    <th className="px-4 py-2 font-light">degradación</th>
                    <th className="px-4 py-2 font-light">degradación score</th>
                  </tr>
                </thead>
                <tbody>
                  {selectedPredictions.length > 0 ? (
                    selectedPredictions.map((prediction, index) => (
                      <tr key={index} className="bg-opacity-15 bg-white">
                        <td className="px-4 py-4">{prediction.date}</td>
                        <td className="px-4 py-4">{prediction.protein_filename.substr(0, prediction.protein_filename.lastIndexOf('.'))}</td>
                        <td className="px-4 py-4">{prediction.toxin_filename.substr(0, prediction.toxin_filename.lastIndexOf('.'))}</td>
                        <td className="px-4 py-4">{prediction.docking_result ? '✔': 'X'}</td>
                        <td className="px-4 py-4 font-extrabold">{prediction.docking_score ? prediction.docking_score.toFixed(4) : '-'}</td>
                        <td className="px-4 py-4">{
                        prediction.degradation_result != null ? 
                          (prediction.degradation_result ? '✔': 'X') : 
                          '-'
                        }</td>
                        <td className="px-4 py-4 font-extrabold">{prediction.degradation_score ? prediction.degradation_score.toFixed(4) : '-'}</td>
                      </tr>
                    ))
                  ) : (
                    <tr>
                      <td colSpan="7" className="px-4 py-8 font-extralight">no se encuentran registros</td>
                    </tr>
                  )}
                </tbody>
              </table>

              {/* Small screens */}
              <div className="md:hidden space-y-6">
                {selectedPredictions.length > 0 ? (
                  selectedPredictions.map((prediction, index) => (
                    <div key={index} className="bg-opacity-15 bg-white rounded-md p-4 text-center text-white pl-8">
                      <p className='font-extralight'>{prediction.date}</p>
                      <p>proteína:
                        <span className="font-thin pl-2">
                        {prediction.protein_filename.substr(0, prediction.protein_filename.lastIndexOf('.'))}
                        </span> 
                      </p>
                      <p>toxina:
                        <span className="font-thin pl-2">
                        {prediction.toxin_filename.substr(0, prediction.toxin_filename.lastIndexOf('.'))}
                        </span> 
                      </p>
                      <p>docking:
                        <span className="font-thin pl-2">
                        {prediction.docking_result ? '✔': 'X'}
                        </span> 
                      </p>
                      <p>docking score:
                        <span className="font-thin pl-2">
                        {prediction.docking_score ? prediction.docking_score.toFixed(4) : '-'}
                        </span> 
                      </p>
                      <p>degradación:
                        <span className="font-thin pl-2">
                        {
                        prediction.degradation_result != null ? 
                          (prediction.degradation_result ? '✔': 'X') : 
                          '-'
                        }
                        </span> 
                      </p>
                      <p>degradación score:
                        <span className="font-thin pl-2">
                        {prediction.degradation_score ? prediction.degradation_score.toFixed(4) : '-'}
                        </span> 
                      </p>
                    </div>
                  ))
                ) : (
                  <p className="px-4 py-8 font-extralight">no se encuentran registros</p>
                )}
              </div>
            </div>
          </div>
        </div>
      </div>
    </>
  );
}