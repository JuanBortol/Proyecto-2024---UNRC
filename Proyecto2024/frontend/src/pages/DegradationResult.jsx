import React, { useContext, useEffect } from 'react';
import { useLocation, useNavigate } from 'react-router-dom';
import Navbar from '../components/Navbar.jsx';
import Check from '../components/Check.jsx';
import styles from '../styles/History.module.css';
import { AppContext } from '../components/AppContext.jsx';

export default function DegradationResult() {
  const { darkMode } = useContext(AppContext);
  // const navigate = useNavigate();
  // const location = useLocation();
  // const results = location.state?.results;

  // useEffect(() => {
  //   if (!results) {
  //     navigate('/');
  //   }
  // }, [navigate, results]);

  const degrades = true; // For testing, will change later

  return (
    <div className={`flex flex-col items-center justify-center text-white min-h-screen space-y-32 
      ${darkMode ? 'bg-black' : (degrades ? styles.bgGreenGradient : styles.bgRedGradient)}`}>
      <Navbar />
      <div className='container space-y-24'>
        {/* Result Section */}
        <div className="flex flex-col items-center w-full space-y-12 px-8">
          <h1 className="text-center text-7xl font-extrabold">degradación</h1>
          {degrades ? (
            <Check strokeWidth="5" className="mr-2 h-16 w-16" />
          ) : (
            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" strokeWidth="5" stroke="currentColor" className="mr-2 h-16 w-16">
              <path strokeLinecap="round" strokeLinejoin="round" d="M6 18 18 6M6 6l12 12" />
            </svg>
          )}
          <p className="text-4xl font-extralight text-center">
            la proteína ingresada <br />
            <strong className="font-bold">{degrades ? 'puede ser degradada' : 'no puede ser degradada'}</strong>
          </p>
        </div>

        {/* Graphs? */}
        {/* <div className="w-full xl:px-8">
          <div className="grid grid-cols-1 mx-12 gap-24 md:mx-24 lg:grid-cols-2 lg:mx-8 xl:mx-32">
            <div className="bg-white p-2">
              <div className='w-full h-72 bg-black flex justify-center items-center'>
                <p className="text-white">
                  Placeholder
                </p>
              </div>
            </div>
            <div className="bg-white p-2">
              <div className='w-full h-72 bg-black flex justify-center items-center'>
                <p className="text-white">Placeholder</p>
              </div>
            </div>
          </div>
        </div> */}
      </div>
    </div>
  );
}