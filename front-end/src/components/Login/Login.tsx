import React, { useState, useEffect } from 'react';
import './Login.css';
import { Link, useNavigate } from 'react-router-dom';
import { ToastContainer, toast } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';
import { useLocation } from 'react-router-dom';


const Login: React.FC = () => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();
  const location = useLocation();
  const [url, setUrl] = useState('https://beetle-upward-yak.ngrok-free.app');


  useEffect(() => {
    // Check if we navigated here after a successful registration
    if (location.state?.fromRegistration) {
      toast.success('Successful Registration. Please log in.', {
        position: "top-right",
        autoClose: 5000,
        hideProgressBar: false,
        closeOnClick: true,
        pauseOnHover: true,
        draggable: true,
        progress: undefined,
      });
    }
  }, [location]);

  useEffect(() => {
    // Check if we navigated here after a successful registration
    if (location.state?.fromCredentials) {
      toast.success('Successfully Changed Credentials. Please log in.', {
        position: "top-right",
        autoClose: 5000,
        hideProgressBar: false,
        closeOnClick: true,
        pauseOnHover: true,
        draggable: true,
        progress: undefined,
      });
    }
  }, [location]);
    

  const handleSubmit = async (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    setLoading(true);
  
    try {
      const response = await fetch(`${url}/login`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ email, password }),
      });
  
      if (!response.ok) {
        toast.error('Login failed. Please check your credentials and try again.', {
          position: "top-right",
          autoClose: 5000,
          hideProgressBar: false,
          closeOnClick: true,
          pauseOnHover: true,
          draggable: true,
          progress: undefined,
        });
        throw new Error('Login failed');
      }
      
  
      const { access_token } = await response.json();
      localStorage.setItem('token', access_token);
      await fetch(`${url}/reset_rasa`, {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('token')}`,
        },
      });
      navigate('/');
    } catch (error) {
      console.error(error);
    } finally {
      setLoading(false);
    }
  };

    
  

  return (
    <div className='login-page-background'>
      <ToastContainer />
      <div className="login-container">
        <form onSubmit={handleSubmit} className="login-form">
          <img src="\images\logo.png" alt='logo' className='logo-img' />
          <h2>Login</h2>
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
          <button type="submit" disabled={loading}>{loading ? 'Logging in...' : 'Login'}</button>
          <Link to="/register">Don't have an account? Register here</Link>
        </form>
      </div>
    </div>
  );
};

export default Login;
