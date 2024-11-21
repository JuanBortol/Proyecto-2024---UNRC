import { useState, useEffect, useContext } from "react";
import { useNavigate } from "react-router-dom";
import DarkModeButton from "../components/DarkModeButton";
import LoginForm from "../components/LoginForm";
import RegistrationForm from "../components/RegistrationForm";
import { AppContext } from "../components/AppContext";

export default function NotLoggedIn() {
  const [showLoginForm, setShowLoginForm] = useState(false);
  const [showRegistrationForm, setShowRegistrationForm] = useState(false);
  const { isAuth, darkMode } = useContext(AppContext);
  const navigate = useNavigate();

  const handleShowLoginButton = () => {
    setShowLoginForm(true);
    setShowRegistrationForm(false);
  };

  const handleShowRegistrationButton = () => {
    setShowRegistrationForm(true);
    setShowLoginForm(false);
  };

  const handleGoBackButton = () => {
    setShowLoginForm(false);
    setShowRegistrationForm(false);
  };

  useEffect(() => {
    if (isAuth) {
      navigate("/home");
    }
  }, [isAuth, navigate]);

  return (
    <div
      className={`flex items-center justify-center min-h-screen ${
        darkMode ? "bg-black" : "bg-gradient-to-b from-[#005F32] to-[#1B3127]"
      }`}
    >
      {(showLoginForm || showRegistrationForm) ? (
        <div className="flex flex-col items-center">
          <button
            className="bg-white font-extralight my-2 py-2 px-2 rounded-full shadow-md focus:outline-none"
            onClick={handleGoBackButton}
          >
            <svg xmlns="http://www.w3.org/2000/svg" 
              fill="none" 
              viewBox="0 0 24 24" 
              strokeWidth="1.5"
              stroke="currentColor" 
              className="size-4">
              <path strokeLinecap="round" strokeLinejoin="round" d="M6.75 15.75 3 12m0 0 3.75-3.75M3 12h18" />
            </svg>
          </button>
          {showLoginForm && <LoginForm />}
          {showRegistrationForm && <RegistrationForm />}
        </div>
      ) : (
        <div className="text-center flex-col space-y-8 flex items-center">
          <h1 className="text-6xl font-bold text-white">PROTEINA UNKNOWN</h1>
          <hr className="border-t-1 border-white w-12 mx-auto" />
          <div className="buttons flex-col space-y-4 flex items-center w-24">
            <button
              className="bg-white text-green-950 font-extralight py-2 rounded-full shadow-md focus:outline-none w-full"
              onClick={handleShowRegistrationButton}
            >
              sign up
            </button>
            <button
              className="bg-white text-green-950 font-extralight py-2 rounded-full shadow-md focus:outline-none w-full"
              onClick={handleShowLoginButton}
            >
              log in
            </button>
          </div>
          <div>
            <DarkModeButton height="32px" />
          </div>
        </div>
      )}
    </div>
  );
}