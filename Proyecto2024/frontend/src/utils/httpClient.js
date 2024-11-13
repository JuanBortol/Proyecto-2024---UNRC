import axios from 'axios';

const apiUrl = process.env.REACT_APP_API_URL || 'http://localhost:5000';

const httpClient = axios.create({
  baseURL: apiUrl,
  withCredentials: true
});

export default httpClient;
