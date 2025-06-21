import React from 'react';
import { Link, useLocation, useNavigate } from 'react-router-dom';
import { useAuth } from './AuthContext';
import './navbar.css';

function Navbar() {
  const location = useLocation();
  const navigate = useNavigate();
  const { user, logout } = useAuth();
  
  // Function to check if a path is active
  const isActive = (path) => {
    return location.pathname === path;
  };

  const handleLogout = () => {
    logout();
    navigate('/');
  };

  return (
    <nav className="navbar">
      <div className="navbar-container">
        <div className="navbar-logo">
          <i className="fas fa-chart-line"></i>
          <Link to="/dashboard">FinTrack</Link>
        </div>
        
        <ul className="navbar-menu">
          <li className="navbar-item">
            <Link to="/dashboard" className={isActive('/dashboard') ? 'active' : ''}>
              Full Dashboard
            </Link>
          </li>
          <li className="navbar-item">
            <Link to="/nocharts" className={isActive('/nocharts') ? 'active' : ''}>
              Simple Dashboard
            </Link>
          </li>
          <li className="navbar-item dropdown">
            <span className="dropdown-toggle">Categories</span>
            <div className="dropdown-menu">
              <Link to="/dashboard?category=Food">Food</Link>
              <Link to="/dashboard?category=Transport">Transport</Link>
              <Link to="/dashboard?category=Entertainment">Entertainment</Link>
              <Link to="/dashboard?category=Utilities">Utilities</Link>
              <Link to="/dashboard?category=Shopping">Shopping</Link>
            </div>
          </li>
          
          {/* User menu */}
          <li className="navbar-item dropdown user-menu">
            <span className="dropdown-toggle user-info">
              <i className="fas fa-user-circle"></i>
              {user ? `${user.first_name} ${user.last_name}` : 'User'}
            </span>
            <div className="dropdown-menu">
              <div className="user-email">{user?.email}</div>
              <div className="dropdown-divider"></div>
              <button onClick={handleLogout} className="logout-btn">
                <i className="fas fa-sign-out-alt"></i> Logout
              </button>
            </div>
          </li>
        </ul>
      </div>
    </nav>
  );
}

export default Navbar;