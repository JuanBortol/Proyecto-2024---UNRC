import React, { createContext, useState, useEffect } from 'react';
import httpClient from '../utils/httpClient';

export const AppContext = createContext();

export const AppProvider = ({ children }) => {
  const [isAuth, setIsAuth] = useState(null);
  const [darkMode, setDarkMode] = useState(false);

  useEffect(() => {
    httpClient
      .get('http://localhost:5000/@me')
      .then((res) => {
        setIsAuth(!!res.data.id); // Check if user auth
      })
      .catch(() => {
        setIsAuth(false);
      });
  }, []);

  useEffect(() => {
    const savedDarkMode = localStorage.getItem('darkMode') === 'true';
    setDarkMode(savedDarkMode);
  }, []);

  const toggleDarkMode = () => {
    setDarkMode((prevMode) => {
      const newMode = !prevMode;
      localStorage.setItem('darkMode', newMode);
      return newMode;
    });
  };

  return (
    <AppContext.Provider
      value={{ isAuth, setIsAuth, darkMode, toggleDarkMode }}
    >
      {children}
    </AppContext.Provider>
  );
};
