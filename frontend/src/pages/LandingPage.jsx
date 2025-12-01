// src/pages/LandingPage.jsx
import React from "react";
import { Link } from "react-router-dom";

const LandingPage = () => {
  const year = new Date().getFullYear();

  return (
    <div className="d-flex flex-column min-vh-100 bg-dark text-light">
      {/* Navbar */}
      <nav className="navbar navbar-expand-lg navbar-dark bg-dark border-bottom border-secondary sticky-top">
        <div className="container">
          {/* Logo */}
          <Link to="/" className="navbar-brand d-flex align-items-center">
            <div
              className="d-flex align-items-center justify-content-center rounded-circle bg-primary text-white fw-bold me-2"
              style={{ width: 32, height: 32, fontSize: 14 }}
            >
              FR
            </div>
            <div className="d-flex flex-column lh-1">
              <span className="small text-uppercase text-muted fw-semibold">
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

          {/* Links + status */}
          <div className="collapse navbar-collapse" id="mainNavbar">
            <ul className="navbar-nav ms-auto mb-2 mb-lg-0 me-3">
              <li className="nav-item">
                <Link to="/" className="nav-link active">
                  Home
                </Link>
              </li>
              <li className="nav-item">
                <Link to="/webcam" className="nav-link">
                  Live Cam
                </Link>
              </li>
              <li className="nav-item">
                <Link to="/upload" className="nav-link">
                  Upload
                </Link>
              </li>
            </ul>

            {/* Status pill */}
            <span className="badge rounded-pill bg-success-subtle text-success d-flex align-items-center gap-2 py-2 px-3">
              <span
                className="rounded-circle bg-success d-inline-block"
                style={{ width: 8, height: 8 }}
              />
              <span className="small">Status: Server OK</span>
            </span>
          </div>
        </div>
      </nav>

      {/* Main content */}
      <main className="flex-grow-1 py-5">
        <div className="container">
          {/* Hero */}
          <section className="text-center mb-5">
            <div className="mx-auto mb-3 d-flex align-items-center justify-content-center rounded-4 bg-primary bg-gradient text-white shadow-lg"
                 style={{ width: 72, height: 72, fontSize: 28 }}>
              <i className="ti-target" />
            </div>
            <h1 className="display-6 fw-bold mb-2">
              Welcome to the <span className="text-primary">FaceReco</span> Project
            </h1>
            <p className="text-muted mx-auto" style={{ maxWidth: 560 }}>
              Identify individuals in real-time using your webcam, or analyze
              uploaded images with our HNSW‑powered face recognition engine.
            </p>
          </section>

          {/* Mode cards */}
          <section className="row g-4 justify-content-center">
            {/* Live Cam */}
            <div className="col-md-6">
              <div className="mode-card h-100 p-4">
                <div className="d-flex align-items-center mb-3 gap-3">
                  <div className="mode-icon-circle bg-primary bg-opacity-25 border border-primary border-opacity-50 text-primary">
                    <i className="ti-video-camera" />
                  </div>
                  <div>
                    <h2 className="h5 mb-1">Live Webcam Mode</h2>
                    <p className="text-muted small mb-0">
                      Real-time detection from your browser camera.
                    </p>
                  </div>
                </div>

                <p className="text-muted small mb-3">
                  Use your connected device for continuous face detection and
                  recognition with low-latency HNSW vector search.
                </p>

                <ul className="text-muted small mb-4 ps-3">
                  <li>Streaming frames directly from webcam.</li>
                  <li>Bounding boxes &amp; labels overlay.</li>
                  <li>Fast nearest-neighbor search via HNSW.</li>
                </ul>

                <Link to="/webcam" className="btn btn-primary rounded-pill">
                  <i className="ti-control-play me-1" />
                  GO TO LIVE
                </Link>
              </div>
            </div>

            {/* Upload */}
            <div className="col-md-6">
              <div className="mode-card h-100 p-4">
                <div className="d-flex align-items-center mb-3 gap-3">
                  <div className="mode-icon-circle bg-info bg-opacity-25 border border-info border-opacity-50 text-info">
                    <i className="ti-upload" />
                  </div>
                  <div>
                    <h2 className="h5 mb-1">Upload Media Mode</h2>
                    <p className="text-muted small mb-0">
                      Analyze static images with multiple faces.
                    </p>
                  </div>
                </div>

                <p className="text-muted small mb-3">
                  Upload captured frames or photos to detect all faces, match
                  them against your student database, and inspect confidence
                  scores.
                </p>

                <ul className="text-muted small mb-4 ps-3">
                  <li>Supports multiple faces per image.</li>
                  <li>Displays per‑match confidence scores.</li>
                  <li>Graceful fallback when no student is found.</li>
                </ul>

                <Link to="/upload" className="btn btn-info rounded-pill text-dark fw-semibold">
                  <i className="ti-arrow-up me-1" />
                  GO TO UPLOAD
                </Link>
              </div>
            </div>
          </section>
        </div>
      </main>

      {/* Footer */}
      <footer className="border-top border-secondary py-3 text-center text-muted small">
        © {year} FaceReco Project · Built with React, Bootstrap 5 &amp; HNSW
      </footer>
    </div>
  );
};

export default LandingPage;
