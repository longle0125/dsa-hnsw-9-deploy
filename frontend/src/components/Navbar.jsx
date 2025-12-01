// src/components/Navbar.jsx
import React from "react";
import { Link, NavLink } from "react-router-dom";
import logoImg from "../assets/logo_dark_cyan.png";

const Navbar = () => {
  return (
      <nav className="navbar navbar-expand-lg navbar-dark bg-dark border-bottom border-secondary sticky-top">
        <div className="container">
          {/* Logo */}
          <Link
            to="/"
            className="navbar-brand d-flex align-items-center text-decoration-none"
          >
            <img
              src={logoImg}
              alt="logo"
              className="me-2"
              style={{ width: 64, height: 32 }}
            />
            <div className="d-flex flex-column lh-1">
              <span className="small text-uppercase fw-semibold">
                FaceReco
              </span>
              <span className="small">HNSW Face Recognition</span>
            </div>
          </Link>

          {/* Toggler (mobile) */}
          <button
            className="navbar-toggler"
            type="button"
            data-bs-toggle="collapse"
            data-bs-target="#mainNavbar"
            aria-controls="mainNavbar"
            aria-expanded="false"
            aria-label="Toggle navigation"
          >
            <span className="navbar-toggler-icon" />
          </button>

          {/* Links */}
          <div className="collapse navbar-collapse" id="mainNavbar">
            <ul className="navbar-nav ms-auto mb-2 mb-lg-0 me-3">
              <li className="nav-item">
                <Link
                  to="/"
                  className="nav-link active text-decoration-none"
                >
                  Home
                </Link>
              </li>
              <li className="nav-item">
                <Link
                  to="/webcam"
                  className="nav-link text-decoration-none"
                >
                  Webcam
                </Link>
              </li>
              <li className="nav-item">
                <Link
                  to="/upload"
                  className="nav-link text-decoration-none"
                >
                  Upload
                </Link>
              </li>
              <li className="nav-item">
                <Link
                  to="/about"
                  className="nav-link text-decoration-none"
                >
                  About
                </Link>
              </li>
            </ul>
          </div>
        </div>
      </nav>
  );
};

export default Navbar;
