// src/pages/NotRegistered.js
import { useState, useContext } from "react";
import { useNavigate } from "react-router-dom";
import RegisterForm from "../components/RegisterForm";
import { AppContext } from "../components/AppContext";
import httpClient from "../utils/httpClient";
import DarkModeButton from "../components/DarkModeButton.jsx";

export default function NotRegistered() {
    const [showRegisterForm, setShowRegisterForm] = useState(false);
    const { darkMode } = useContext(AppContext);
    const navigate = useNavigate();

    const handleShowRegisterButton = () => {
        setShowRegisterForm(true);
    };

    const handleGoBackButton = () => {
        setShowRegisterForm(false);
    };

    const handleRegisterSubmit = async (formData) => {
        try {
            const response = await httpClient.post('http://localhost:5000/register', {
                username: formData.username,
                password: formData.password,
                confirm_password: formData.confirm_password,
            });
            if (response.status === 200) {
                console.log('Register successful');
                navigate('/', { state: { results: response.data } });
            }
        } catch (error) {
            alert(`ERROR: ${error.response?.data?.error || 'Ocurrió un error'}`);
            navigate("/");
        }
    };


    return (
        <div
            className={`flex items-center justify-center min-h-screen ${
                darkMode ? "bg-black" : "bg-gradient-to-b from-[#005F32] to-[#1B3127]"
            }`}
        >
            {showRegisterForm ? (
                <div className="flex flex-col items-center">
                    <button
                        className="bg-white font-extralight my-2 py-2 px-2 rounded-full shadow-md focus:outline-none"
                        onClick={handleGoBackButton}
                    >
                        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" strokeWidth="1.5" stroke="currentColor" className="size-4">
                            <path strokeLinecap="round" strokeLinejoin="round" d="M6.75 15.75 3 12m0 0 3.75-3.75M3 12h18" />
                        </svg>
                    </button>

                    {/* Usar RegisterForm */}
                    <RegisterForm onSubmit={handleRegisterSubmit} />
                </div>
            ) : (
                <div className="text-center flex-col space-y-8 flex items-center">
                    <h1 className="text-6xl font-bold text-white">PROTEINA</h1>
                    <hr className="border-t-1 border-white w-12 mx-auto"/>
                    <button
                        className="bg-white text-green-950 font-extralight py-2 px-8 rounded-full shadow-md focus:outline-none"
                        onClick={handleShowRegisterButton}
                    >
                        registrarse
                    </button>
                    <div>
                        <DarkModeButton height="32px"/>
                    </div>
                </div>
            )}
        </div>
    );
}
