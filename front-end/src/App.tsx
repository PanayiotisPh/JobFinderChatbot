import React from 'react';
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import Home from './components/Home/Home';
import Login from './components/Login/Login';
import Register from './components/Register/Register';
import { Navigate, Outlet } from "react-router-dom";

const ProtectedRoute = () => {
  // Check if the user has a token
  const token = localStorage.getItem('token');

  if (!token) {
    return <Navigate to="/login" />;
  }
  
  return <Outlet />;
  
};

const App = () => {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<ProtectedRoute />}>
          <Route index element={<Home />} /> {/* Protected Home Page */}
          {/* Any other protected routes go here */}
        </Route>
        <Route path="/login" element={<Login />} /> {/* Public Login Page */}
        <Route path="/register" element={<Register />} /> {/* Public Register Page */}
        {/* Redirect or 404 Page Not Found can also be placed here */}
      </Routes>
    </BrowserRouter>
  );
};

export default App;
