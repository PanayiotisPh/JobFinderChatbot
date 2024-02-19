import React, { useState } from 'react';
import './Register.css';
import { Link } from 'react-router-dom';

const Register: React.FC = () => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const [username, setUsername] = useState('');
  const handleSubmit = (event: React.FormEvent) => {
    event.preventDefault();
    // Here you would typically handle the register logic, 
    // like calling an API with the email and password
    console.log('Register Submitted', { email, password });
  };

  return (
    <div className='register-page-background'>
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
              type="confirm-password"
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
