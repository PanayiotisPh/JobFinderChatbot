import React, { ReactNode } from 'react';
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import Home from './components/Home/Home';
import Login from './components/Login/Login';
import Register from './components/Register/Register';
import { Navigate, Outlet } from "react-router-dom";
import ChatHistory from './components/ChatHistory/ChatHistory';
import Chat from './components/Chat/Chat';
import ChangeCredentials from './components/ChangeCredentials/ChangeCredentials';
import CvDetails from './components/CVDetails/CvDetails';

interface ProtectedRouteProps {
  children: ReactNode;
}

const ProtectedRoute: React.FC<ProtectedRouteProps> = ({ children }) => {
  const token = localStorage.getItem('token');
  return token ? <>{children}</> : <Navigate to="/login" />;
};

const App = () => {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<ProtectedRoute><Home /></ ProtectedRoute>}>
            <Route index element={<Chat key={window.location.pathname} />} />
            <Route path="chat/:chatId" element={<ChatHistory />} />
            <Route path="/change-credentials" element={<ChangeCredentials />} />
            <Route path="/cv-details" element={<CvDetails />} />
        </Route>
        <Route path="/login" element={<Login />} />
        <Route path="/register" element={<Register />} />
        <Route path="*" element={<Navigate to="/login" replace />} />
      </Routes>
    </BrowserRouter>
  );
};

export default App;
