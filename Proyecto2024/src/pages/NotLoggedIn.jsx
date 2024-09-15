import { useState, useEffect } from 'react';
import DarkModeButton from '../components/DarkModeButton';
import LoginForm from '../components/LoginForm';
import styles from '../styles/NotLoggedIn.module.css';
import { useNavigate } from 'react-router-dom';

export default function NotLoggedIn() {
  const [showLoginForm, setShowLoginForm] = useState(false); // Toggle login form

  const handleLoginClick = () => {
    setShowLoginForm(true);
  };
  const navigate = useNavigate();
 
  useEffect(() => {
    const username = sessionStorage.getItem('username');
    if (username) {
      navigate('/home');
    }
  }, [navigate]);

  return (
    <div className={`flex items-center justify-center min-h-screen ${styles.bgGradient}`}>
      {showLoginForm ? (
        <LoginForm />
      ) : (
        <div className="text-center flex-col space-y-8 flex items-center">
          <h1 className="text-6xl font-bold text-white">PROTEINA</h1>
          <hr className="border-t-1 border-white w-12 mx-auto" />
          <button
            className="bg-white text-green-950 font-extralight py-2 px-8 rounded-full shadow-md focus:outline-none"
            onClick={handleLoginClick}
          >
            log in
          </button>
          <div>
            <DarkModeButton height="32px" />
          </div>
        </div>
      )}
    </div>
  );
}