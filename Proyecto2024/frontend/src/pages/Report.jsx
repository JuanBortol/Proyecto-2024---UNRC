import React, { useState, useContext } from 'react';
import { useNavigate } from 'react-router-dom';
import Navbar from '../components/Navbar';
import httpClient from '../utils/httpClient';
import styles from '../styles/History.module.css';
import { AppContext } from '../components/AppContext';

export default function Report() {
  const { darkMode } = useContext(AppContext);
  const navigate = useNavigate();
  const [proteinFile, setProteinFile] = useState(null);
  const [pdfFile, setPdfFile] = useState(null);
  const [toxinFile, setToxinFile] = useState(null);
  const [reason, setReason] = useState('');

  const handleFileChange = (e, setFile) => {
    const file = e.target.files[0];
    if (file) {
      setFile(file);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    if (!proteinFile || !reason) {
      alert('Debe cargar la protein y proveer una descripción del error.');
      return;
    }
  
    const formData = new FormData();
    formData.append('protein_file', proteinFile);
    formData.append('pdf_file', pdfFile);
    formData.append('toxin_file', toxinFile);
    formData.append('reason', reason);
  
    try {
      const response = await httpClient.post('http://localhost:5000/submit_report', formData, {
        headers: { 'Content-Type': 'multipart/form-data' },
      });
      
      if (response.status === 200) {
        alert('Tu reporte ha sido enviado');
        navigate('/'); // to be changed 
      }
    } catch (error) {
      alert(`ERROR: ${error.response.data.error}`);
    }
  };

  return (
    <div
      className={`flex items-center justify-center text-white min-h-screen 
      ${darkMode ? 'bg-black' : styles.bgGreenGradient}`}
    >
      <Navbar />
      <div className="container min-h-full my-24 space-y-12 md:space-y-24 xl:space-y-48 px-8 max-w-xl">
        <h1 className="text-center text-7xl font-extrabold">reportar</h1>
        <div className="justify-center font-light">
          <p className='text-center py-2 font-extralight'>*la carga del archivo PDF es opcional.</p>
          <form
            onSubmit={handleSubmit}
            encType="multipart/form-data"
            className="flex flex-col mx-auto space-y-8"
          >
            <div className='buttons flex-col space-y-4'>
              <div className='upperButtons flex space-x-4'>
                  <button
                    type="button"
                    className={`
                      w-full py-2 px-8  rounded-full bg-white text-green-950 flex justify-center items-center
                      ${proteinFile !== null ? 'bg-gray-300 bg-opacity-50 text-gray-800 cursor-not-allowed' : 'bg-white text-black'}`}
                      onClick={() => document.getElementById('proteinInput').click()}
                      disabled={proteinFile !== null}
                    >
                    {proteinFile !== null ?
                    <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" className='mr-2 h-4 w-4'>
                    <path d="m4.5 12.75 6 6 9-13.5"/>
                    </svg>            
                    :
                    <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24"  stroke="currentColor" className="mr-2 h-4 w-4">
                      <path strokeLinecap="round" strokeLinejoin="round" d="M13.19 8.688a4.5 4.5 0 0 1 1.242 7.244l-4.5 4.5a4.5 4.5 0 0 1-6.364-6.364l1.757-1.757m13.35-.622 1.757-1.757a4.5 4.5 0 0 0-6.364-6.364l-4.5 4.5a4.5 4.5 0 0 0 1.242 7.244" />
                    </svg>
                    }
                      cargar proteina (.pdb)
                  </button>
                  <input
                    type="file"
                    id="proteinInput"
                    name="protein_file"
                    accept=".pdb"
                    style={{ display: 'none' }}
                    onChange={(e) => handleFileChange(e, setProteinFile)}
                  />
                  <button
                    type="button"
                    className={`w-full py-2 px-8 rounded-full bg-white text-green-950 flex justify-center items-center
                    ${toxinFile !== null ? 'bg-gray-300 bg-opacity-50 text-gray-800 cursor-not-allowed' : 'bg-white text-black'}`}
                    onClick={() => document.getElementById('toxinInput').click()}
                    disabled={toxinFile !== null}
                  >
                    {toxinFile !== null ? 
                    <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" className='mr-2 h-4 w-4'>
                    <path d="m4.5 12.75 6 6 9-13.5"/>
                    </svg>            
                    :
                    <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" strokeWidth={1.5} stroke="currentColor" className="mr-2 h-4 w-4">
                      <path strokeLinecap="round" strokeLinejoin="round" d="M9 8.25H7.5a2.25 2.25 0 0 0-2.25 2.25v9a2.25 2.25 0 0 0 2.25 2.25h9a2.25 2.25 0 0 0 2.25-2.25v-9a2.25 2.25 0 0 0-2.25-2.25H15m0-3-3-3m0 0-3 3m3-3V15" />
                    </svg>
                    }
                    cargar toxina (.sdf)
                  </button>
                  <input
                    type="file"
                    id="toxinInput"
                    name="toxin_file"
                    accept=".sdf"
                    style={{ display: 'none' }}
                    onChange={(e) => handleFileChange(e, setToxinFile)}
                  />
              </div>
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
                  <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" strokeWidth="1.5" stroke="currentColor" className="mr-2 h-4 w-4">
                    <path strokeLinecap="round" strokeLinejoin="round" d="M19.5 14.25v-2.625a3.375 3.375 0 0 0-3.375-3.375h-1.5A1.125 1.125 0 0 1 13.5 7.125v-1.5a3.375 3.375 0 0 0-3.375-3.375H8.25m2.25 0H5.625c-.621 0-1.125.504-1.125 1.125v17.25c0 .621.504 1.125 1.125 1.125h12.75c.621 0 1.125-.504 1.125-1.125V11.25a9 9 0 0 0-9-9Z" />
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
                    onChange={(e) => handleFileChange(e, setPdfFile)}
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