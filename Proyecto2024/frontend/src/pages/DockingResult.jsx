import React, { useRef, useContext, useEffect, useState } from 'react';
import { useLocation, useNavigate } from 'react-router-dom';
import Navbar from '../components/Navbar.jsx';
import Check from '../components/Check.jsx';
import PredictionLoading from '../components/PredictionLoading.jsx';
import styles from '../styles/History.module.css';
import { AppContext } from '../components/AppContext.jsx';
import httpClient from "../utils/httpClient.js";

export default function DockingResult() {
  const { darkMode } = useContext(AppContext);
  const navigate = useNavigate();
  const location = useLocation();
  const results = location.state?.results;
  const PREDICT_SERVICE_URL = import.meta.env.VITE_PREDICT_SERVICE_URL;

  // State for model selection
  const [selectedModel, setSelectedModel] = useState("default"); // "default" or "custom"
  const [fileName, setFileName] = useState(null);
  const [isSubmitting, setIsSubmitting] = useState(false);

  const fileInputModelRef = useRef(null);

  useEffect(() => {
    if (!results) {
      navigate('/');
    }
  }, [navigate, results]);

  const handleModelButtonClick = () => {
    if (fileInputModelRef.current) {
      fileInputModelRef.current.click();
    }
  };

  const handleModelChange = (event) => {
    const file = event.target.files[0];
    setFileName(file ? file.name : null);
  };

  const docking = results.docking_result;

  const handleSubmit = async () => {
    if (selectedModel === "custom" && !fileName) {
      console.error('No hay un modelo cargado.');
      alert('Por favor, carga un modelo personalizado o selecciona el modelo predeterminado.');
      return;
    }

    if (!results.createPrediction.prediction_id) {
      console.error('No se ha encontrado un ID de predicción válido.');
      alert('Error: No hay una predicción válida.');
      return;
    }

    setIsSubmitting(true);

    const formData = new FormData();

    if (selectedModel === "default") {
      formData.append('model_file', 'mi_modelo.h5');
    } else if (selectedModel === "custom" && fileInputModelRef.current.files[0]) {
      formData.append('model_file', fileInputModelRef.current.files[0]);
    }

    formData.append('protein_filepath', results.protein_filepath)
    formData.append('toxin_filepath', results.toxin_filepath)

    try {
      const response = await httpClient.post(`${PREDICT_SERVICE_URL}/submit_model`, formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });

      if (response.status === 200) {
        console.log('Model submission successful');
        const { degradation_result, degradation_score } = response.data;
  
        const updatePredictionResponse = await httpClient.put('/predictions',
          {
            prediction_id: results.createPrediction.prediction_id,
            degradation_result,
            degradation_score
          }
        );
  
        if (updatePredictionResponse.status === 200) {
          console.log('Prediction entry updated successfully');
          navigate('/degradation_result', { state: { results: response.data } });
        }
      }
    } catch (error) {
      console.error('Error during request:', error.response || error.message);
      alert(`ERROR: ${error.response ? error.response.data.error : error.message}`);
      navigate('/');
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <>
    <div className={`flex flex-col items-center justify-center text-white min-h-screen space-y-32 
      ${darkMode ? 'bg-black' : (docking ? styles.bgGreenGradient : styles.bgRedGradient)}`}>
      <Navbar />
      <div className='container space-y-24'>
        {/* Result Section */}
        <div className="flex flex-col items-center w-full space-y-12 px-8">
          <h1 className="text-center text-7xl font-extrabold">resultado</h1>
          {docking ? (
            <Check strokeWidth="5" className="mr-2 h-16 w-16" />
          ) : (
            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" strokeWidth="5" stroke="currentColor" className="mr-2 h-16 w-16">
              <path strokeLinecap="round" strokeLinejoin="round" d="M6 18 18 6M6 6l12 12" />
            </svg>
          )}
          <p className="text-4xl font-extralight text-center">
            la proteína ingresada <br />
            <strong className="font-bold">{docking ? 'es capaz de realizar docking' : 'no realiza docking'}</strong>
          </p>
        </div>

        {/* Docking Score Section */}
        <div className="w-full xl:px-8">
          <div className="grid grid-cols-1 mx-12 gap-24 md:mx-24 lg:grid-cols-2 lg:mx-8 xl:mx-32">
            <div className="bg-white p-2">
              <div className='w-full h-72 bg-black flex justify-center items-center'>
                <p className="text-white">
                  {docking ? `Docking score: ${results.docking_score}` : "Placeholder"}
                </p>
              </div>
            </div>
            <div className="bg-white p-2">
              <div className='w-full h-72 bg-black flex justify-center items-center'>
                <p className="text-white">Placeholder</p>
              </div>
            </div>
          </div>

          {/* Model Selection */}
          {docking && (
            <div className="flex flex-col items-center py-8 space-y-8">
              <div className='text-center'>
                <h2 className='text-4xl font-semibold'>selecciona tu modelo</h2>
                <p className='font-light'>(para predecir degradación)</p>
              </div>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4 w-full max-w-3xl">
                {/* Default Model */}
                <div
                  className={`cursor-pointer transition-all duration-300 rounded-lg p-6 flex flex-col items-center justify-center h-40 
                    ${selectedModel === "default"
                      ? 
                        (darkMode ? 
                          'bg-gray-800 border-gray-700'
                          :
                          "bg-emerald-700 border-emerald-500"
                        )
                      : (darkMode ? 
                          'bg-gray-800/20 border-gray-700/20 hover:bg-gray-700/50'
                          :
                          "bg-emerald-800/50 border-emerald-700 hover:bg-emerald-700/50"
                        )
                    } border`}
                  onClick={() => setSelectedModel("default")}
                >
                  <h3 className="text-xl font-semibold text-white/90 mb-2">
                    modelo predeterminado
                  </h3>
                  <p className="text-white/75 text-center mb-4 font-thin">
                    utilizá nuestro modelo preentrenado
                  </p>
                  {selectedModel === "default" && (
                      <Check className="h-4 w-4" strokeWidth="2.5"/>
                  )}
                </div>

                {/* Custom Model*/}
                <div
                  className={`cursor-pointer transition-all duration-300 rounded-lg p-6 flex flex-col items-center justify-center h-40 
                    ${selectedModel === "custom"
                      ? 
                        (darkMode ? 
                          'bg-gray-800 border-gray-700'
                          :
                          "bg-emerald-700 border-emerald-500"
                        )
                      : (darkMode ? 
                          'bg-gray-800/20 border-gray-700/20 hover:bg-gray-700/50'
                          :
                          "bg-emerald-800/50 border-emerald-700 hover:bg-emerald-700/50"
                        )
                    } border`}
                  onClick={() => setSelectedModel("custom")}
                >
                  <h3 className="text-xl font-semibold text-white/90 mb-2">
                    modelo personalizado
                  </h3>
                  <p className="text-white/75 text-center mb-4 font-thin">
                    subí tu propio modelo entrenado
                  </p>
                  {selectedModel === "custom" && (
                      <Check className="h-4 w-4" strokeWidth="2.5"/>
                  )}
                </div>
              </div>

              {/* File Upload */}
              {selectedModel === "custom" && (
                <div className="w-full max-w-md flex flex-col items-center">
                  <input
                    id="model-upload"
                    type="file"
                    ref={fileInputModelRef}
                    onChange={handleModelChange}
                    className="hidden"
                  />
                  <button
                    onClick={handleModelButtonClick}
                    className={`sm:w-64 bg-white 
                      ${darkMode ? 
                        'text-black hover:bg-gray-400/20 hover:text-white'
                        :
                        'text-emerald-900 hover:bg-emerald-600/50 hover:text-emerald-100'
                      } py-2 px-4 rounded flex items-center justify-center transition-colors duration-200
                      ${fileName ? 'cursor-pointer' : ''}
                    `}
                  >
                    <span>subir modelo</span>
                  </button>
                  {fileName && (
                    <p className="mt-2 text-center text-gray-300 font-thin">seleccionado: <strong>{fileName}</strong></p>
                  )}
                </div>
              )}

              {/* Submit button */}
              <button
                  className="px-4 font-light rounded-full py-2 bg-white text-green-950"
                  onClick={handleSubmit}
              >
                <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" className='w-6 h-6'>
                  <path strokeLinecap="round" strokeLinejoin="round" d="M17.25 8.25 21 12m0 0-3.75 3.75M21 12H3" />
                </svg>
              </button>
            </div>
          )}
        </div>
      </div>
    </div>
    {isSubmitting ? <PredictionLoading /> : null}
    </>
  );
}
