import React from 'react';
import './NavBar.css';

export function Navbar() {
  return (
    <nav className="custom-navbar ">
      <div className="navbar-left">
      </div>
      <div className="navbar-right">
        <ul className="navbar-links">
          <li><a href="/">Home</a></li>
          <li><a href="/previous-scripts">Model Analytics</a></li>
          <li><a href="/">Related News</a></li>
        </ul>
      </div>
    </nav>
  );
}