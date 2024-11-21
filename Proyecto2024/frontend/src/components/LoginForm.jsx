import { useState, useContext } from 'react';
import { useNavigate } from 'react-router-dom';
import DarkModeButton from './DarkModeButton';
import httpClient from '../utils/httpClient';
import { AppContext } from './AppContext';

export default function LoginForm() {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState(null);
  const { setIsAuth } = useContext(AppContext);
  const navigate = useNavigate();

  const handleLogin = async (e) => {
    e.preventDefault();

    try {
      const response = await httpClient.post('/login', {
        username,
        password,
      });
      localStorage.setItem('username', response.data.username);
      setIsAuth(true);
      navigate('/home');
    } catch (error) {
      if (error.response && error.response.status === 400) {
        setError(error.response.data.message);
      } else {
        setError('Ha ocurrido un error, intentalo nuevamente más tarde.');
      }
    }
  };

  return (
    <div className="flex items-center justify-center flex-col">
      {error && (
        <div
          className="bg-red-600 bg-opacity-45   text-white px-4 py-3 rounded my-2"
          role="alert"
        >
          <span className="block sm:inline font-light">{error}</span>
        </div>
      )}
      <div className="w-full max-w-md p-4 space-y-6">
        <form onSubmit={handleLogin} className="space-y-4">
          <div>
            <label
              htmlFor="username"
              className="block text-sm font-extralight text-white"
            ></label>
            <input
              type="text"
              id="username"
              placeholder="username"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              className="mt-1 py-1 px-4 block w-full rounded-full border-gray-300 shadow-sm font-light"
              required
            />
          </div>
          <div>
            <label
              htmlFor="password"
              className="block text-sm font-extralight text-white"
            ></label>
            <input
              type="password"
              id="password"
              placeholder="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              className="mt-1 py-1 px-4 block w-full rounded-full border-gray-300 shadow-sm font-light"
              required
            />
          </div>
          <button
            type="submit"
            className="w-full py-1 text-white rounded-full font-light hover:font-normal"
          >
            log in
          </button>
        </form>
        <DarkModeButton className="mx-auto" />
      </div>
    </div>
  );
}
