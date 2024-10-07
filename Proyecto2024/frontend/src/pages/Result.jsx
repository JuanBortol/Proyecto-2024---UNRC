import React, { useRef, useContext, useEffect, useState } from 'react';
import { useLocation, useNavigate } from 'react-router-dom';
import Navbar from '../components/Navbar';
import styles from '../styles/History.module.css';
import { AppContext } from '../components/AppContext';
import httpClient from "../utils/httpClient.js";

export default function Report() {
  const { darkMode } = useContext(AppContext);
  const navigate = useNavigate();
  const location = useLocation();
  const results = location.state?.results;
  const fileInputModelRef = useRef(null);
  const [modelFilename, setModelFilename] = useState("modelo predeterminado"); // Modelo predeterminado

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
    if (file) {
      setModelFilename(file.name);
    } else {
      setModelFilename("modelo predeterminado"); // Restablece al modelo predeterminado si no hay archivo
    }
  };


  if (!results) {
    return null;
  }
  const docking = results.result;

  const submitModel = async () => {
    if (!modelFilename) {
      console.error('No hay un modelo cargado.');
      return;
    }

    const formData = new FormData();
    const modelFile = fileInputModelRef.current.files[0];
    if (modelFile) formData.append('model_file', modelFile);

    try {
      const response = await httpClient.post('http://localhost:5000/submit_model', formData);
      console.log(response.status);
      if (response.status === 200) {
        console.log('Model submission successful');
        navigate('/degradation');
      }
    } catch (error) {
      console.error('Error en la solicitud:', error);
      alert(`ERROR: ${error.response ? error.response.data : error.message}`);
      setModelFilename(modelFile);
      navigate('/');
    }
  };


  return (
      <div className={`flex flex-col items-center justify-center text-white min-h-screen space-y-32 
      ${darkMode ? 'bg-black' : (docking ? styles.bgGreenGradient : styles.bgRedGradient)}`}>
        <Navbar />
        <div className='container space-y-24'>
          <div className="flex flex-col items-center w-full space-y-12 px-8">
            <h1 className="text-center text-7xl font-extrabold">resultado</h1>
            {docking ? (
                <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth="5" className="mr-2 h-16 w-16">
                  <path d="m4.5 12.75 6 6 9-13.5" />
                </svg>
            ) : (
                <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" strokeWidth="5" stroke="currentColor" className="mr-2 h-16 w-16">
                  <path strokeLinecap="round" strokeLinejoin="round" d="M6 18 18 6M6 6l12 12" />
                </svg>
            )}
            <p className="text-4xl font-extralight text-center">
              la proteina ingresada <br />
              <strong className="font-bold">{docking ? 'es capaz de realizar docking' : 'no realiza docking'}</strong>
            </p>
          </div>
          <div className="w-full xl:px-8">
            <div className="grid grid-cols-1 mx-12 gap-24 md:mx-24 lg:grid-cols-2 lg:mx-8 xl:mx-32">
              <div className="bg-white p-2">
                <div className='w-full h-72 bg-black flex justify-center items-center'>
                  <p>{docking ? `Docking score: ${results.docking_score}` : 1}</p>
                </div>
              </div>
              <div className="bg-white p-2">
                <div className='w-full h-72 bg-black flex justify-center items-center'>
                  <p>Placeholder</p>
                </div>
              </div>
            </div>
            <div className="flex justify-center py-8">
              <input
                  type="file"
                  ref={fileInputModelRef}
                  onChange={handleModelChange}
                  style={{display: 'none'}}
              />
              <div
                  className="flex flex-col items-center py-8 space-y-4">
                <input
                    type="file"
                    ref={fileInputModelRef}
                    onChange={handleModelChange}
                    style={{display: 'none'}}
                />
                <button
                    type="button"
                    className={`sm:w-80 w-full h-10 py-2 flex items-center justify-center rounded-full transition-colors duration-250
                    ${modelFilename !== "modelo predeterminado"
                        ? 'bg-gray-300 bg-opacity-10 text-gray-300 cursor-not-allowed'
                        : 'bg-transparent text-white hover:bg-white hover:text-green-950'}
                    `}
                    onClick={handleModelButtonClick}
                    disabled={modelFilename !== "modelo predeterminado"}
                >
                  <span>{modelFilename}</span>
                </button>

                <button
                    type="button"
                    className="sm:w-64 py-2 px-8 rounded-full bg-white text-green-950 flex justify-center items-center font-light"
                    onClick={submitModel}
                >
                  <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" strokeWidth={1}
                       stroke="currentColor" className="mr-2 w-4 h-4">
                    <path strokeLinecap="round" strokeLinejoin="round" d="m8.25 4.5 7.5 7.5-7.5 7.5"/>
                  </svg>
                  predecir degradación
                </button>
              </div>

            </div>
          </div>
        </div>
      </div>
  );
}
