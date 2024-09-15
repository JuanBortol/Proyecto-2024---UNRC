import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import NotLoggedIn from './pages/NotLoggedIn';
import LoggedIn from './pages/LoggedIn';
import Logout from './components/Logout';

function AppRouter() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<NotLoggedIn />} />
        <Route path="/home" element={<LoggedIn />} />
        <Route path="/logout" element={<Logout />} />
      </Routes>
    </Router>
  );
}

export default AppRouter;
