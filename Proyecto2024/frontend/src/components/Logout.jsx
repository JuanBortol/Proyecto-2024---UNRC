import { useState, useEffect, useContext } from 'react';
import { useNavigate } from 'react-router-dom';
import httpClient from '../utils/httpClient';
import { AppContext } from './AppContext';
import Loading from './Loading';

export default function Logout() {
  const navigate = useNavigate();
  const { isAuth, setIsAuth } = useContext(AppContext);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (isAuth) {
      httpClient.post('/logout')
        .then(res => {
          localStorage.removeItem('username');
          setIsAuth(false);
          navigate('/');
        })
        .catch((e) => {
          console.error(e);
        })
        .finally(() => {
          setLoading(false);
        });
    } else {
      navigate('/');
    }
  }, [isAuth, navigate, setIsAuth]);

  if (loading) return <Loading />;
}
