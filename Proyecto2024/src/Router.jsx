import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import NotLoggedIn from './pages/NotLoggedIn';
import LoggedIn from './pages/LoggedIn';
import Logout from './components/Logout';
import PrivateRoute from './components/PrivateRoute';

function AppRouter() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<NotLoggedIn />} />
        <Route path="/logout" element={<Logout />} />

        <Route element={<PrivateRoute />}>
          <Route path="/home" element={<LoggedIn />} />
          <Route path="/history" element={<History />} />
        </Route>
      </Routes>
    </Router>
  );
}

export default AppRouter;
