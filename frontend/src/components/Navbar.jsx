// src/components/Navbar.jsx
import React, { useEffect, useState } from "react";
import { Link, NavLink } from "react-router-dom";
import logoImg from "../assets/logo_dark_cyan.png";

const Navbar = () => {
  const [mode, setMode] = useState("hnsw"); // "hnsw" | "bruteforce"

  // Đọc chế độ từ localStorage khi load
  useEffect(() => {
    const saved = window.localStorage.getItem("searchMode");
    if (saved === "hnsw" || saved === "bruteforce") {
      setMode(saved);
    }
  }, []);

  // Lưu lại mỗi khi đổi
  const handleChangeMode = (newMode) => {
    setMode(newMode);
    window.localStorage.setItem("searchMode", newMode);
  };

  return (
    <nav className="navbar navbar-expand-lg navbar-dark bg-dark border-bottom border-secondary sticky-top">
      <div className="container">
        {/* Logo bên trái */}
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
            <span className="small text-uppercase fw-semibold text-info">HNSW</span>
            <span className="small">Face Recognition</span>
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

        {/* Menu + Mode switch bên phải */}
        <div className="collapse navbar-collapse" id="mainNavbar">
          {/* NAV LINKS CENTER */}
          <ul className="navbar-nav mx-auto gap-3">
            <li className="nav-item">
              <NavLink
                to="/"
                end
                className={({ isActive }) =>
                  `nav-link fw-bold ${
                    isActive ? "text-info" : "text-light"
                  }`
                }
              >
                Home
              </NavLink>
            </li>

            <li className="nav-item">
              <NavLink
                to="/webcam"
                className={({ isActive }) =>
                  `nav-link fw-bold ${
                    isActive ? "text-info" : "text-light"
                  }`
                }
              >
                Webcam
              </NavLink>
            </li>

            <li className="nav-item">
              <NavLink
                to="/upload"
                className={({ isActive }) =>
                  `nav-link fw-bold ${
                    isActive ? "text-info" : "text-light"
                  }`
                }
              >
                Upload
              </NavLink>
            </li>

            <li className="nav-item">
              <NavLink
                to="/about"
                className={({ isActive }) =>
                  `nav-link fw-bold ${
                    isActive ? "text-info" : "text-light"
                  }`
                }
              >
                About
              </NavLink>
            </li>
          </ul>

          {/* BÊN PHẢI: Chế độ tìm kiếm */}
          <div className="d-flex align-items-center ms-lg-3">
            <span className="small text-muted me-2 d-none d-md-inline">
              {/* Chế độ tìm kiếm: */}
            </span>
            <div className="btn-group btn-group-sm" role="group" aria-label="Search mode">
              <button
                type="button"
                className={
                  "btn fw-semibold " +
                  (mode === "hnsw"
                    ? "btn-info text-dark"
                    : "btn-outline-info text-light")
                }
                onClick={() => handleChangeMode("hnsw")}
              >
                HNSW
              </button>
              <button
                type="button"
                className={
                  "btn fw-semibold " +
                  (mode === "bruteforce"
                    ? "btn-info text-dark"
                    : "btn-outline-info text-light")
                }
                onClick={() => handleChangeMode("bruteforce")}
              >
                Brute‑force
              </button>
            </div>
          </div>
        </div>
      </div>
    </nav>
  );
};

export default Navbar;
