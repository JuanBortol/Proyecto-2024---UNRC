import React, { useState, useContext } from 'react';
import Navbar from '../components/Navbar';
import httpClient from '../utils/httpClient';
import styles from '../styles/History.module.css';
import { AppContext } from '../components/AppContext';

export default function Report() {
  const { darkMode } = useContext(AppContext);
  const [chainFile, setChainFile] = useState(null);
  const [pdfFile, setpdfFile] = useState(null);
  const [reason, setReason] = useState('');

  const handleFileChange = (e, setFile) => {
    const file = e.target.files[0];
    if (file) {
      setFile(file);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    if (!chainFile || !reason) {
      alert('Debe cargar la cadena y proveer una descripción del error.');
      return;
    }
  
    const formData = new FormData();
    formData.append('chain_file', chainFile);
    formData.append('pdf_file', pdfFile);
    formData.append('reason', reason);
  
    try {
      const response = await httpClient.post('http://localhost:5000/submit_report', formData, {
        headers: { 'Content-Type': 'multipart/form-data' },
      });
      
      if (response.status === 200) {
        console.log('Report successfully submitted');
      } else {
        console.error(`Error: ${response.data.error}`);
      }
    } catch (error) {
      console.error('Error submitting the report:', error);
      alert('An error occurred while submitting the report.');
    }
  };

  return (
    <div
      className={`flex items-center justify-center text-white min-h-screen 
      ${darkMode ? 'bg-black' : styles.bgGradient}`}
    >
      <Navbar />
      <div className="container space-y-48 px-8 max-w-xl">
        <h1 className="text-center text-7xl font-extrabold">reportar</h1>
        <div className="justify-center font-light">
          <p className='text-center py-2 font-extralight'>*la carga del archivo PDF es opcional.</p>
          <form
            onSubmit={handleSubmit}
            encType="multipart/form-data"
            className="flex flex-col mx-auto space-y-8"
          >
            <div className='buttons flex space-x-4'>
                <button
                  type="button"
                  className={`
                    w-full py-2 px-8  rounded-full bg-white text-green-950 flex justify-center items-center
                    ${chainFile !== null ? 'bg-gray-300 bg-opacity-50 text-gray-800 cursor-not-allowed' : 'bg-white text-black'}`}
                    onClick={() => document.getElementById('chainInput').click()}
                    disabled={chainFile !== null}
                  >
                  {chainFile !== null ? 
                  <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" className='mr-2 h-4 w-4'>
                  <path d="m4.5 12.75 6 6 9-13.5"/>
                  </svg>            
                  :
                  <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24"  stroke="currentColor" class="mr-2 h-4 w-4">
                    <path stroke-linecap="round" stroke-linejoin="round" d="M13.19 8.688a4.5 4.5 0 0 1 1.242 7.244l-4.5 4.5a4.5 4.5 0 0 1-6.364-6.364l1.757-1.757m13.35-.622 1.757-1.757a4.5 4.5 0 0 0-6.364-6.364l-4.5 4.5a4.5 4.5 0 0 0 1.242 7.244" />
                  </svg>
                  }
                    cargar cadena
                </button>
                <input
                  type="file"
                  id="chainInput"
                  name="chain_file"
                  accept=".txt"
                  style={{ display: 'none' }}
                  onChange={(e) => handleFileChange(e, setChainFile)}
                />
                <button
                  type="button"
                  className={`w-full py-2 px-8 rounded-full bg-white text-green-950 flex justify-center items-center
                  ${pdfFile !== null ? 'bg-gray-300 bg-opacity-50 text-gray-800 cursor-not-allowed' : 'bg-white text-black'}`}
                  onClick={() => document.getElementById('pdfInput').click()}
                  disabled={pdfFile !== null}
                >
                  {pdfFile !== null ? 
                  <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" className='mr-2 h-4 w-4'>
                  <path d="m4.5 12.75 6 6 9-13.5"/>
                  </svg>            
                  :
                  <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="mr-2 h-4 w-4">
                    <path stroke-linecap="round" stroke-linejoin="round" d="M19.5 14.25v-2.625a3.375 3.375 0 0 0-3.375-3.375h-1.5A1.125 1.125 0 0 1 13.5 7.125v-1.5a3.375 3.375 0 0 0-3.375-3.375H8.25m2.25 0H5.625c-.621 0-1.125.504-1.125 1.125v17.25c0 .621.504 1.125 1.125 1.125h12.75c.621 0 1.125-.504 1.125-1.125V11.25a9 9 0 0 0-9-9Z" />
                  </svg>
                  }
                  cargar pdf
                </button>
                <input
                  type="file"
                  id="pdfInput"
                  name="pdf_file"
                  accept=".pdf"
                  style={{ display: 'none' }}
                  onChange={(e) => handleFileChange(e, setpdfFile)}
                />
            </div>

            <hr className="border-t-1 border-white w-12 mx-auto" />
            <div className="reason flex flex-col">
              <label htmlFor="reason">motivo (máx. 500 caracteres):</label>
              <textarea
                id="reason"
                name="reason"
                rows="4"
                value={reason}
                onChange={(e) => setReason(e.target.value)}
                maxLength="500"
                placeholder="describe brevemente el error"
                className="resize-none text-black px-2 w-full rounded-md"
                required
              />
              <button 
                type="submit"
                className="mx-auto py-2 text-white font-extralight hover:font-normal"
              >
                reportar
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>
  );
}