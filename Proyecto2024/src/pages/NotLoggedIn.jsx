import { useState, useEffect, useContext } from "react";
import { useNavigate } from "react-router-dom";
import DarkModeButton from "../components/DarkModeButton";
import LoginForm from "../components/LoginForm";
import { AppContext } from "../components/AppContext";

export default function NotLoggedIn() {
  const [showLoginForm, setShowLoginForm] = useState(false); // Toggle login form
  const { isAuth, darkMode } = useContext(AppContext);
  const navigate = useNavigate();

  const handleLoginClick = () => {
    setShowLoginForm(true);
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