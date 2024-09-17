import React, { useState, useContext } from 'react';
import Navbar from '../components/Navbar';
import httpClient from '../utils/httpClient';
import styles from '../styles/History.module.css';
import { AppContext } from '../components/AppContext';

export default function Report() {
  const { darkMode } = useContext(AppContext);

  return (
    <div
      className={`flex flex-col items-center justify-center text-white min-h-screen space-y-32 
      ${darkMode ? 'bg-black' : styles.bgGradient}`}
    >
      <Navbar />
      <div className='container space-y-24'>
        <div className="flex flex-col items-center w-full  space-y-12 px-8">
          <h1 className="text-center text-7xl font-extrabold">resultado</h1>
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
          <p className="text-4xl font-extralight text-center">
            la proteina ingresada <br />
            <strong className="font-bold">
              es capaz de unirse y degradar aflatoxina
            </strong>
          </p>
        </div>
        <div className="w-full bg-gray-400 bg-opacity-15 xl:px-8">
          <div className="grid grid-cols-1 mx-12 gap-24 md:mx-24 lg:grid-cols-2 lg:mx-8 xl:mx-32">
            <div className="bg-white p-2">
              <div className='w-full h-72 bg-black flex justify-center items-center'>
                <p> 1</p>
              </div>
            </div>
            <div className="bg-white p-2">
              <div className='w-full h-72 bg-black flex justify-center items-center'>
                <p> 2</p>
              </div>
            </div>
            <div className="bg-white p-2">
              <div className='w-full h-72 bg-black flex justify-center items-center'>
                <p> 3</p>
              </div>
            </div>
            <div className="bg-white p-2">
              <div className='w-full h-72 bg-black flex justify-center items-center'>
                <p> 4</p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
