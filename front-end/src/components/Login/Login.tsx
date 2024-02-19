import React, { useState } from 'react';
import './Login.css';
import { Link } from 'react-router-dom';

const Login: React.FC = () => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');

  const handleSubmit = (event: React.FormEvent) => {
    event.preventDefault();
    // Here you would typically handle the login logic, 
    // like calling an API with the email and password
    console.log('Login Submitted', { email, password });
  };

  return (
    <div className='login-page-background'>
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
          <button type="submit">Login</button>
          <Link to="/register">Don't have an account? Register here</Link>
        </form>
      </div>
    </div>
  );
};

export default Login;
