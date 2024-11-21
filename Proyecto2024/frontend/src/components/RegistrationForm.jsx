import { useState } from 'react';
import DarkModeButton from './DarkModeButton';
import httpClient from '../utils/httpClient';

export default function RegistrationForm() {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const [message, setMessage] = useState(null);
  const [isSuccess, setIsSuccess] = useState(false);

  const handleRegistration = async (e) => {
    e.preventDefault();

    try {
      const response = await httpClient.post('/register', {
        username,
        password,
        confirm_password: confirmPassword,
      });
      setMessage(response.data.message);
      setIsSuccess(true);
      
      setTimeout(() => {
        setMessage(null);
        setIsSuccess(false);
      }, 5000);
    } catch (error) {
      setIsSuccess(false);
      if (error.response && error.response.status === 400) {
        setMessage(error.response.data.message);
      } else {
        setMessage('Ha ocurrido un error, intentalo nuevamente más tarde.');
      }
    }
  };

  return (
    <div className="flex items-center justify-center flex-col">
      {message && (
        <div
          className={`${
            isSuccess ? 'bg-green-600' : 'bg-red-600'
          } bg-opacity-45 text-white px-4 py-3 rounded my-2`}
          role="alert"
        >
          <span className="block sm:inline font-light">{message}</span>
        </div>
      )}
      <div className="w-full max-w-md p-4 space-y-6">
        <form onSubmit={handleRegistration} className="space-y-4">
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
          <div>
            <label
              htmlFor="confirmPassword"
              className="block text-sm font-extralight text-white"
            ></label>
            <input
              type="password"
              id="confirmPassword"
              placeholder="confirm password"
              value={confirmPassword}
              onChange={(e) => setConfirmPassword(e.target.value)}
              className="mt-1 py-1 px-4 block w-full rounded-full border-gray-300 shadow-sm font-light"
              required
            />
          </div>
          <button
            type="submit"
            className="w-full py-1 text-white rounded-full font-light hover:font-normal"
          >
            sign up
          </button>
        </form>
        <DarkModeButton className="mx-auto" />
      </div>
    </div>
  );
}