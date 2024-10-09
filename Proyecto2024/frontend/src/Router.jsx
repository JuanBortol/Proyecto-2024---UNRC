import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import NotLoggedIn from './pages/NotLoggedIn';
import LoggedIn from './pages/LoggedIn';
import Logout from './components/Logout';
import History from './pages/History';
import Report from './pages/Report';
import PrivateRoute from './components/PrivateRoute';
import DockingResult from './pages/DockingResult';
import DegradationResult from './pages/DegradationResult';

function AppRouter() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<NotLoggedIn />} />
        <Route path="/logout" element={<Logout />} />

        <Route element={<PrivateRoute />}>
          <Route path="/home" element={<LoggedIn />} />
          <Route path="/history" element={<History />} />
          <Route path="/report" element={<Report />} />
          <Route path="/docking_result" element={<DockingResult />} />
          <Route path="/degradation_result" element={<DegradationResult />} />
        </Route>
      </Routes>
    </Router>
  );
}

export default AppRouter;
