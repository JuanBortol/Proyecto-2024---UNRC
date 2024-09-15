import { useEffect, useRef, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import Navbar from "../components/Navbar";
import styles from '../styles/LoggedIn.module.css';
import httpClient from '../httpClient';

export default function LoggedIn() {
  const navigate = useNavigate();
  const username = sessionStorage.getItem('username');

  // hidden file inputs
  const fileInputChainRef = useRef(null);
  const fileInputModelRef = useRef(null);

  const [chainFilename, setChainFilename] = useState(null);
  const [modelFilename, setModelFilename] = useState(null);
  const [isSubmitting, setIsSubmitting] = useState(false);

  const [chainButtonDisabled, setChainButtonDisabled] = useState(false);
  const [modelButtonDisabled, setModelButtonDisabled] = useState(false);

  useEffect(() => {
    if (!username) {
      navigate('/');
    }
  }, [username, navigate]);

  useEffect(() => {
    setChainButtonDisabled(!!chainFilename);
    setModelButtonDisabled(!!modelFilename);
  }, [chainFilename, modelFilename]);

  if (!username) return null;

  const handleFileChainUpload = async (event) => {
    const file = event.target.files[0];
    if (file) {
      setChainFilename(file.name);
      const formData = new FormData();
      formData.append('file', file);
      formData.append('type', 'chain');

      try {
        const response = await httpClient.post('http://localhost:5000/upload', formData);
        if (response.status === 200) {
          console.log("File selected successfully.");
        } else {
          console.error("File selection failed.");
        }
      } catch (error) {
        console.error('Error selecting file:', error);
      }
    }
  };

  const handleFileModelUpload = async (event) => {
    const file = event.target.files[0];
    if (file) {
      setModelFilename(file.name);
      const formData = new FormData();
      formData.append('file', file);
      formData.append('type', 'model');

      try {
        const response = await httpClient.post('http://localhost:5000/upload', formData);
        if (response.status === 200) {
          console.log("File selected successfully.");
        } else {
          console.error("File selection failed.");
        }
      } catch (error) {
        console.error('Error selecting file:', error);
      }
    }
  };

  const handleSubmit = async () => {
    if (!chainFilename || !modelFilename) {
      return;
    }
    setIsSubmitting(true);
    const formData = new FormData();
    const chainFile = fileInputChainRef.current.files[0];
    const modelFile = fileInputModelRef.current.files[0];

    if (chainFile) formData.append('chain_file', chainFile);
    if (modelFile) formData.append('model_file', modelFile);

    try {
      const response = await httpClient.post('http://localhost:5000/submit', formData);
      if (response.status === 200) {
        console.log('Submission successful');
        navigate('/');
      } else {
        console.error('Submission failed');
      }
    } catch (error) {
      console.error('Error submitting files:', error);
    } finally {
      setIsSubmitting(false);
    }
  };

  const handleChainButtonClick = () => {
    fileInputChainRef.current.click();
  };

  const handleModelButtonClick = () => {
    fileInputModelRef.current.click();
  };

  return (
    <>
      <div className={`${styles.bgGradient} flex items-center justify-center text-white min-h-screen space-y-16`}>
        <Navbar />
        <div className='container space-y-36'>
          <div className='top-text space-y-2'>
            <h1 className='text-7xl text-white'>bienvenid@<strong className='font-black'>, {username}</strong></h1>
            <h2 className='text-4xl font-thin'>provea la información necesaria para continuar</h2>
          </div>
          <div className='buttons flex justify-around text-2xl font-light text-green-950 space-x-8'>
            {/* Chain button */}
            <button 
              className={`w-full ${chainButtonDisabled ? 'bg-green-300 text-gray-800 cursor-not-allowed' : 'bg-white text-black'} rounded-full py-2 flex items-center justify-center`}
              onClick={handleChainButtonClick}
              disabled={chainButtonDisabled}
            >
              {chainButtonDisabled ? 
              <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" className='mr-2 h-6 w-6'>
              <path d="m4.5 12.75 6 6 9-13.5"/>
              </svg>            
              :
               <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" className="w-6 h-6 mr-2">
                <path d="M19.5 14.25v-2.625a3.375 3.375 0 0 0-3.375-3.375h-1.5A1.125 1.125 0 0 1 13.5 7.125v-1.5a3.375 3.375 0 0 0-3.375-3.375H8.25m0 12.75h7.5m-7.5 3H12M10.5 2.25H5.625c-.621 0-1.125.504-1.125 1.125v17.25c0 .621.504 1.125 1.125 1.125h12.75c.621 0 1.125-.504 1.125-1.125V11.25a9 9 0 0 0-9-9Z" />
              </svg>}
              cargar cadena
            </button>
            {/* Model button */}
            <button 
              className={`w-full ${modelButtonDisabled ? 'bg-green-400 bg-opacity-15 text-gray-300 cursor-not-allowed' : 'bg-transparent text-white hover:bg-white hover:text-green-950'} py-2 flex items-center justify-center rounded-full transition-colors duration-250`}
              onClick={handleModelButtonClick}
              disabled={modelButtonDisabled}
            >
              {modelButtonDisabled ? 
              <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" className='mr-2 h-6 w-6'>
              <path d="m4.5 12.75 6 6 9-13.5"/>
              </svg>            
              :
              <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" className="w-6 h-6 mr-2">
                <path d="M3 16.5v2.25A2.25 2.25 0 0 0 5.25 21h13.5A2.25 2.25 0 0 0 21 18.75V16.5m-13.5-9L12 3m0 0 4.5 4.5M12 3v13.5" />
              </svg>}
              cargar modelo
            </button>
            {/* Hidden file inputs */}
            <input
              type="file"
              ref={fileInputChainRef}
              style={{ display: 'none' }}
              onChange={handleFileChainUpload}
            />
            <input
              type="file"
              ref={fileInputModelRef}
              style={{ display: 'none' }}
              onChange={handleFileModelUpload}
            />
            <button 
              className={`${modelButtonDisabled && chainButtonDisabled ? 'bg-white text-green-950' : 'bg-gray-300 bg-opacity-15 text-gray-300 cursor-not-allowed'} px-3 font-light rounded-full py-2`}
              onClick={handleSubmit}
              disabled={isSubmitting}
            >
              <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" className='w-6 h-6'>
                <path d="M17.25 8.25 21 12m0 0-3.75 3.75M21 12H3" />
              </svg>
            </button>
          </div>
        </div>
      </div>
    </>
  );
}
