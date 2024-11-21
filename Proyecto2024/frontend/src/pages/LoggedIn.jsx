import { useRef, useState, useContext } from 'react';
import { useNavigate } from 'react-router-dom';
import Navbar from "../components/Navbar";
import Check from '../components/Check';
import styles from '../styles/LoggedIn.module.css';
import httpClient from '../utils/httpClient';
import { AppContext } from '../components/AppContext';
import PredictionLoading from '../components/PredictionLoading';

export default function LoggedIn() {
  const navigate = useNavigate();
  const username = localStorage.getItem('username');
  const { darkMode } = useContext(AppContext);

  // hidden file inputs
  const fileInputProteinRef = useRef(null);
  const fileInputToxinRef = useRef(null);

  const [proteinFilename, setProteinFilename] = useState(null);
  const [toxinFilename, setToxinFilename] = useState(null);
  const [isSubmitting, setIsSubmitting] = useState(false);

  const handleFileProteinUpload = async (event) => {
    const file = event.target.files[0];
    if (file) {
      if (file.name.split('.').pop() !== 'pdb') {
        console.error("Por favor, selecciona un archivo .pdb para la proteína.");
        setProteinFilename(null); // Reiniciar el nombre del archivo
        return;
      }

      setProteinFilename(file.name);
      const formData = new FormData();
      formData.append('file', file);
      formData.append('type', 'protein');

      try {
        const response = await httpClient.post('/upload', formData);
        if (response.status === 200) {
          console.log("Archivo de proteína seleccionado con éxito.");
        } else {
          console.error("La selección del archivo de proteína falló.");
        }
      } catch (error) {
        console.error('Error al seleccionar el archivo de proteína:', error);
      }
    }
  };

  const handleFileToxinUpload = async (event) => {
    const file = event.target.files[0];
    if (file) {
      if (file.name.split('.').pop() !== 'sdf') {
        console.error("Por favor, selecciona un archivo .sdf para la toxina.");
        setToxinFilename(null); // Reiniciar el nombre del archivo
        return;
      }

      setToxinFilename(file.name);
      const formData = new FormData();
      formData.append('file', file);
      formData.append('type', 'toxin');

      try {
        const response = await httpClient.post('/upload', formData);
        if (response.status === 200) {
          console.log("Archivo de toxina seleccionado con éxito.");
        } else {
          console.error("La selección del archivo de toxina falló.");
        }
      } catch (error) {
        console.error('Error al seleccionar el archivo de toxina:', error);
      }
    }
  };

  const handleSubmit = async () => {
    if (!proteinFilename || !toxinFilename) {
      console.error('Both files must be selected.');
      return;
    }
  
    setIsSubmitting(true);
    const formData = new FormData();
    const proteinFile = fileInputProteinRef.current.files[0];
    const toxinFile = fileInputToxinRef.current.files[0];
  
    if (proteinFile) formData.append('protein_file', proteinFile);
    if (toxinFile) formData.append('toxin_file', toxinFile);
  
    try {
      const response = await httpClient.post('/submit', formData);
  
      if (response.status === 200) {
        console.log('Submission successful');
        const { docking_result, docking_score, protein_filepath, toxin_filepath } = response.data;
  
        const createPredictionResponse = await httpClient.post('/predictions',
          {
            protein_filename: proteinFilename,
            protein_filepath,
            toxin_filename: toxinFilename,
            toxin_filepath,
            docking_result,
            docking_score,
          }
        );
  
        if (createPredictionResponse.status === 201) {
          console.log('Prediction entry created successfully');
          navigate('/docking_result', { 
            state: { 
              results: { 
                ...response.data, 
                createPrediction: createPredictionResponse.data 
              } 
            } 
          });
        }
      }
    } catch (error) {
      alert(`ERROR: ${error.response?.data?.error || 'An unexpected error occurred.'}`);
      setProteinFilename(null);
      setToxinFilename(null);
      navigate('/'); // to be changed
    } finally {
      setIsSubmitting(false);
    }
  };  

  const handleProteinButtonClick = () => {
    fileInputProteinRef.current.click();
  };

  const handleToxinButtonClick = () => {
    fileInputToxinRef.current.click();
  };
  return (
      <>
        <div className={`flex items-center justify-center text-white min-h-screen space-y-16  ${darkMode ? "bg-black" : styles.bgGradient}`}>
          <Navbar />
          <div className='container min-h-full py-12 my-24 space-y-12 md:space-y-36 px-4'>
            <div className='top-text space-y-2'>
              <h1 className='text-7xl text-white'>bienvenid@<strong className='font-black'>, {username}</strong></h1>
              <h2 className='text-4xl font-thin'>provea la información necesaria para continuar</h2>
            </div>
            <div className=
            'buttons flex flex-col items-center md:flex-row md:justify-around md:space-y-0 md:space-x-8 text-2xl font-light text-green-950 space-y-4'
            >
              {/* Protein button */}
              <button
                  className={`w-full rounded-full py-2 flex items-center justify-center
                ${proteinFilename !== null ? 'bg-gray-300 bg-opacity-50 text-gray-800 cursor-not-allowed' : 'bg-white text-black'}
              `}
                  onClick={handleProteinButtonClick}
                  disabled={proteinFilename !== null}
              >
                {proteinFilename !== null ?
                    <Check className='mr-2 h-6 w-6' />
                    :
                    <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24"  stroke="currentColor" className="mr-2 h-6 w-6">
                      <path strokeLinecap="round" strokeLinejoin="round" d="M13.19 8.688a4.5 4.5 0 0 1 1.242 7.244l-4.5 4.5a4.5 4.5 0 0 1-6.364-6.364l1.757-1.757m13.35-.622 1.757-1.757a4.5 4.5 0 0 0-6.364-6.364l-4.5 4.5a4.5 4.5 0 0 0 1.242 7.244" />
                    </svg>
                }
                cargar proteina (.pdb)
              </button>
              {/* Toxin button */}
              <button
                  className={`w-full py-2 flex items-center justify-center rounded-full transition-colors duration-250
              ${toxinFilename !== null ?
                      'bg-gray-300 bg-opacity-10 text-gray-300 cursor-not-allowed'
                      :
                      'bg-transparent text-white hover:bg-white hover:text-green-950'}
              `}
                  onClick={handleToxinButtonClick}
                  disabled={toxinFilename !== null}
              >
                {toxinFilename !== null ?
                    <Check className='mr-2 h-6 w-6' />
                    :
                    <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" className="w-6 h-6 mr-2">
                      <path d="M3 16.5v2.25A2.25 2.25 0 0 0 5.25 21h13.5A2.25 2.25 0 0 0 21 18.75V16.5m-13.5-9L12 3m0 0 4.5 4.5M12 3v13.5" />
                    </svg>}
                cargar toxina (.sdf)
              </button>
              {/* Hidden file inputs */}
              <input
                  type="file"
                  ref={fileInputProteinRef}
                  style={{ display: 'none' }}
                  onChange={handleFileProteinUpload}
              />
              <input
                  type="file"
                  ref={fileInputToxinRef}
                  style={{ display: 'none' }}
                  onChange={handleFileToxinUpload}
              />
              <button
                  className={`px-3 font-light rounded-full py-3
                ${toxinFilename !== null && proteinFilename !== null ?
                      'bg-white text-green-950'
                      :
                      'bg-gray-300 bg-opacity-15 text-gray-300 cursor-not-allowed'}
                `}
                  onClick={handleSubmit}
                  disabled={isSubmitting || !(toxinFilename !== null && proteinFilename !== null)}
              >
                <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" className='w-6 h-6'>
                  <path strokeLinecap="round" strokeLinejoin="round" d="M17.25 8.25 21 12m0 0-3.75 3.75M21 12H3" />
                </svg>
              </button>
            </div>
          </div>
        </div>
        {isSubmitting ? <PredictionLoading /> : null}
      </>
  );
}
