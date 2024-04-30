import React, { useState } from 'react';
import './Register.css';
import { Link, useNavigate } from 'react-router-dom';
import { ToastContainer, toast } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';

const Register: React.FC = () => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const [username, setUsername] = useState('');
  const navigate = useNavigate();
  const [url, setUrl] = useState(' https://beetle-upward-yak.ngrok-free.app');


    // Construct the user data
  const userData = {
    username,
    email,
    password,
  };

  const handleSubmit = async (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault();

    if (password !== confirmPassword) {
      toast.error('Register failed. Password and Confirm password do not match.', {
        position: "top-right",
        autoClose: 5000,
        hideProgressBar: false,
        closeOnClick: true,
        pauseOnHover: true,
        draggable: true,
        progress: undefined,
      });
      return;
    }

    try {
      const response = await fetch(`${url}/register`, { // Change URL to your backend endpoint
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(userData),
      });

      if (response.ok) {
        navigate('/login',  { state: { fromRegistration: true } });
      } else if (response.status === 400) {
        toast.error('Email already in use', {
          position: "top-right",
          autoClose: 5000,
          hideProgressBar: false,
          closeOnClick: true,
          pauseOnHover: true,
          draggable: true,
          progress: undefined,
        });
      } else {
        // Handle server-side validation errors
        const errorData = await response.json();
        alert(`Registration failed: ${errorData.message || "Unknown error"}`);
      }
    } catch (error) {
      alert('An error occurred during registration. Please try again.');
    }
  };

  return (
    <div className='register-page-background'>
      <ToastContainer />
      <div className="register-container">
        <form onSubmit={handleSubmit} className="register-form">
          <img src="\images\logo.png" alt='logo' className='logo-img' />
          <h2>Register</h2>
          <div className="form-group">
            <label htmlFor="username">Username:</label>
            <input
              type="username"
              id="username"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              required
            />
          </div>
          <div className="form-group">
            <label htmlFor="email">Email:</label>
            <input
              type="email"
              id="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              required
            />
          </div>
          <div className="form-group">
            <label htmlFor="password">Password:</label>
            <input
              type="password"
              id="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
            />
          </div>
          <div className="form-group">
            <label htmlFor="confirm-password">Confirm Password:</label>
            <input
              type="password"
              id="confirm-password"
              value={confirmPassword}
              onChange={(e) => setConfirmPassword(e.target.value)}
              required
            />
          </div>
          <button type="submit">Register</button>
          <Link to="/login">Already have an account? Login here</Link>
        </form>
      </div>
    </div>
  );
};

export default Register;
