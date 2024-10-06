import React, { useContext, useEffect } from 'react';
import {useLocation, useNavigate} from 'react-router-dom';
import Navbar from '../components/Navbar';
import styles from '../styles/History.module.css';
import { AppContext } from '../components/AppContext';

export default function Report() {
  const { darkMode } = useContext(AppContext);
  const navigate = useNavigate();
  const location = useLocation(); // Get location object
  const results = location.state?.results; // Extract results from the location state
  useEffect(() => {
    if (!results) {
        navigate('/');
    }
    }, [navigate, results]);

    if (!results) {
        return null;
    }

    const docking = results.result;

  return (
    <div
      className={`flex flex-col items-center justify-center text-white min-h-screen space-y-32 
      ${darkMode ? 'bg-black' : (docking ? styles.bgGreenGradient : styles.bgRedGradient)}`}
    >
      <Navbar />
      <div className='container space-y-24'>
        <div className="flex flex-col items-center w-full space-y-12 px-8">
          <h1 className="text-center text-7xl font-extrabold">resultado</h1>
          {docking ? 
          <svg
            xmlns="http://www.w3.org/2000/svg"
            fill="none"
            viewBox="0 0 24 24"
            stroke="currentColor"
            strokeWidth="5"
            className="mr-2 h-16 w-16"
          >
            <path d="m4.5 12.75 6 6 9-13.5" />
          </svg>
          :
          <svg 
            xmlns="http://www.w3.org/2000/svg" 
            fill="none" 
            viewBox="0 0 24 24" 
            strokeWidth="5" 
            stroke="currentColor" 
            className="mr-2 h-16 w-16"
        >
            <path strokeLinecap="round" strokeLinejoin="round" d="M6 18 18 6M6 6l12 12" />
          </svg>
          }
          <p className="text-4xl font-extralight text-center">
            la proteina ingresada <br />
            <strong className="font-bold">
                {docking ? 'es capaz de realizar docking' : 'no realiza docking'}
            </strong>
          </p>
        </div>
        <div className="w-full xl:px-8">
          <div className="grid grid-cols-1 mx-12 gap-24 md:mx-24 lg:grid-cols-2 lg:mx-8 xl:mx-32">
            <div className="bg-white p-2">
              <div className='w-full h-72 bg-black flex justify-center items-center'>
                <p>{docking ? `Docking score: ${results.docking_score}` 
                :
                1
                }</p>
              </div>
            </div>
            <div className="bg-white p-2">
              <div className='w-full h-72 bg-black flex justify-center items-center'>
                <p>Placeholder</p>
              </div>
            </div>
          </div>
        <div className={`${docking ? '':'hidden'} flex justify-center py-8`}>
        <button
          type="button"
          className={`sm:w-64 my-4 py-2 px-8 rounded-full bg-white text-green-950 flex justify-center items-center font-light`}
          // onClick={}     to be changed
        >
          <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" strokeWidth={1} stroke="currentColor" className="mr-2 w-4 h-4">
            <path strokeLinecap="round" strokeLinejoin="round" d="m8.25 4.5 7.5 7.5-7.5 7.5" />
          </svg>
          predecir degradación
        </button>
        </div>
        </div>
      </div>
    </div>
  );
}