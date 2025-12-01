// src/App.jsx
import React from "react";
import { BrowserRouter, Routes, Route } from "react-router-dom";

import LandingPage from "./pages/LandingPage";
import UploadPage from "./pages/UploadPage";
import WebcamPage from "./pages/WebcamPage";

export default function App() {
    return (
        <BrowserRouter>
            <Routes>
                <Route path="/" element={<LandingPage />} />
                <Route path="/upload" element={<UploadPage />} />
                <Route path="/webcam" element={<WebcamPage />} />
            </Routes>
        </BrowserRouter>
    );
}
