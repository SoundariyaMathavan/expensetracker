import React from 'react';
import { Link } from 'react-router-dom';
import { useAuth } from './AuthContext';
import './home-page.css';

function HomePage() {
  const { isAuthenticated } = useAuth();

  return (
    <div className="home-container">
      <header className="home-header">
        <div className="logo">
          <i className="fas fa-chart-line"></i>
          <h1>FinTrack</h1>
        </div>
        <nav className="main-nav">
          <ul>
            <li><Link to="/" className="active">Home</Link></li>
            {isAuthenticated() ? (
              <>
                <li><Link to="/dashboard">Dashboard</Link></li>
                <li><Link to="/nocharts">Simple Dashboard</Link></li>
              </>
            ) : (
              <>
                <li><Link to="/login">Login</Link></li>
                <li><Link to="/signup">Sign Up</Link></li>
              </>
            )}
            <li><a href="#features">Features</a></li>
            <li><a href="#about">About</a></li>
          </ul>
        </nav>
      </header>

      <section className="hero">
        <div className="hero-content">
          <h1>Take Control of Your Finances</h1>
          <p>Track, analyze, and optimize your spending with our powerful financial dashboard</p>
          <div className="cta-buttons">
            {isAuthenticated() ? (
              <Link to="/dashboard" className="btn btn-primary">View Dashboard</Link>
            ) : (
              <Link to="/signup" className="btn btn-primary">Get Started</Link>
            )}
            <a href="#features" className="btn btn-secondary">Learn More</a>
          </div>
        </div>
        <div className="hero-image">
          <img src="https://via.placeholder.com/600x400?text=Financial+Dashboard" alt="Dashboard Preview" />
        </div>
      </section>

      <section id="features" className="features">
        <h2>Powerful Features</h2>
        <div className="feature-grid">
          <div className="feature-card">
            <div className="feature-icon">
              <i className="fas fa-chart-pie"></i>
            </div>
            <h3>Expense Tracking</h3>
            <p>Easily track and categorize all your expenses in one place</p>
          </div>
          <div className="feature-card">
            <div className="feature-icon">
              <i className="fas fa-chart-bar"></i>
            </div>
            <h3>Visual Analytics</h3>
            <p>Understand your spending patterns with intuitive charts and graphs</p>
          </div>
          <div className="feature-card">
            <div className="feature-icon">
              <i className="fas fa-lightbulb"></i>
            </div>
            <h3>Smart Recommendations</h3>
            <p>Get personalized tips to improve your financial health</p>
          </div>
          <div className="feature-card">
            <div className="feature-icon">
              <i className="fas fa-filter"></i>
            </div>
            <h3>Category Filters</h3>
            <p>Drill down into specific spending categories for detailed analysis</p>
          </div>
        </div>
      </section>

      <section id="about" className="about">
        <div className="about-content">
          <h2>About FinTrack</h2>
          <p>FinTrack is a powerful financial dashboard that helps you understand and optimize your spending habits. Our mission is to make financial management accessible and insightful for everyone.</p>
          <p>With FinTrack, you can:</p>
          <ul>
            <li>Track expenses across different categories</li>
            <li>Visualize spending patterns over time</li>
            <li>Get personalized recommendations to save money</li>
            <li>Make informed financial decisions based on data</li>
          </ul>
        </div>
      </section>

      <section className="dashboard-preview">
        <h2>Choose Your Dashboard</h2>
        <div className="dashboard-options">
          <div className="dashboard-option">
            <h3>Full Dashboard</h3>
            <p>Complete analytics with interactive charts and detailed insights</p>
            <img src="https://via.placeholder.com/400x250?text=Full+Dashboard" alt="Full Dashboard" />
            <Link to="/dashboard" className="btn btn-primary">Open Full Dashboard</Link>
          </div>
          <div className="dashboard-option">
            <h3>Simple Dashboard</h3>
            <p>Streamlined view with essential metrics and basic visualizations</p>
            <img src="https://via.placeholder.com/400x250?text=Simple+Dashboard" alt="Simple Dashboard" />
            <Link to="/nocharts" className="btn btn-primary">Open Simple Dashboard</Link>
          </div>
        </div>
      </section>

      <footer className="home-footer">
        <div className="footer-content">
          <div className="footer-logo">
            <i className="fas fa-chart-line"></i>
            <h2>FinTrack</h2>
          </div>
          <div className="footer-links">
            <h3>Quick Links</h3>
            <ul>
              <li><Link to="/">Home</Link></li>
              <li><Link to="/dashboard">Dashboard</Link></li>
              <li><Link to="/nocharts">Simple Dashboard</Link></li>
              <li><a href="#features">Features</a></li>
              <li><a href="#about">About</a></li>
            </ul>
          </div>
          <div className="footer-contact">
            <h3>Contact Us</h3>
            <p>Email: support@fintrack.example</p>
            <p>Phone: (123) 456-7890</p>
            <div className="social-icons">
              <a href="https://facebook.com" target="_blank" rel="noopener noreferrer" aria-label="Facebook">
                <i className="fab fa-facebook"></i>
              </a>
              <a href="https://twitter.com" target="_blank" rel="noopener noreferrer" aria-label="Twitter">
                <i className="fab fa-twitter"></i>
              </a>
              <a href="https://instagram.com" target="_blank" rel="noopener noreferrer" aria-label="Instagram">
                <i className="fab fa-instagram"></i>
              </a>
              <a href="https://linkedin.com" target="_blank" rel="noopener noreferrer" aria-label="LinkedIn">
                <i className="fab fa-linkedin"></i>
              </a>
            </div>
          </div>
        </div>
        <div className="copyright">
          <p>&copy; 2023 FinTrack. All rights reserved.</p>
        </div>
      </footer>
    </div>
  );
}

export default HomePage;
