import { useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import httpClient from '../httpClient';

export default function Logout() {
  const navigate = useNavigate();

  useEffect(() => {
    const handleLogout = async () => {
      try {
        await httpClient.post('http://localhost:5000/logout', {});
        sessionStorage.removeItem('username')
        navigate('/');
      } catch (error) {
        console.error('Logout failed:', error);
      }
    };
    handleLogout();
  }, [navigate]);
}
