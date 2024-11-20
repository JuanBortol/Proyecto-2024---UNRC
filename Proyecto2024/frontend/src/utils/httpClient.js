import axios from 'axios';

const apiUrl = import.meta.env.VITE_API_URL;

const httpClient = axios.create({
  baseURL: apiUrl,
  withCredentials: true
});

export default httpClient;
