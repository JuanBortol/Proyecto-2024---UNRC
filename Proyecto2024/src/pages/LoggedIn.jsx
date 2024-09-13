import { useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import Navbar from "../components/Navbar";
import styles from '../styles/LoggedIn.module.css'

export default function LoggedIn() {
  const navigate = useNavigate();
  const username = sessionStorage.getItem('username');

  useEffect(() => {
    if (!username) {
      navigate('/');
    }
  }, [username, navigate]);

  if (!username) return null; 

    return (
        <>
      <div className={`${styles.bgGradient} flex items-center justify-center text-white min-h-screen space-y-16`}>
        <Navbar />
        <div className='container space-y-36'>
          <div className='top-text space-y-2'>
            <h1 className='text-7xl text-white'>bienvenid@<strong className='font-black'>, {username}</strong>
            </h1>
            <h2 className='text-4xl font-thin'>provea la información necesaria para continuar</h2>
          </div>
          <div className='buttons flex justify-around text-2xl font-light text-green-950 space-x-8'>
            <button className='w-full bg-white rounded-full py-2 flex items-center justify-center'>
            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" className="w-6 h-6 mr-2">
              <path d="M19.5 14.25v-2.625a3.375 3.375 0 0 0-3.375-3.375h-1.5A1.125 1.125 0 0 1 13.5 7.125v-1.5a3.375 3.375 0 0 0-3.375-3.375H8.25m0 12.75h7.5m-7.5 3H12M10.5 2.25H5.625c-.621 0-1.125.504-1.125 1.125v17.25c0 .621.504 1.125 1.125 1.125h12.75c.621 0 1.125-.504 1.125-1.125V11.25a9 9 0 0 0-9-9Z" />
            </svg>
            cargar cadena</button>
            <button className='w-full bg-transparent text-white py-2 flex items-center justify-center transition-colors duration-250 hover:bg-white hover:text-green-950 rounded-full'>
              <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" className="w-6 h-6 mr-2">
                <path d="M3 16.5v2.25A2.25 2.25 0 0 0 5.25 21h13.5A2.25 2.25 0 0 0 21 18.75V16.5m-13.5-9L12 3m0 0 4.5 4.5M12 3v13.5" />
              </svg>
              cargar modelo
            </button>
          </div>
        </div>
      </div>
    </>
    );
}