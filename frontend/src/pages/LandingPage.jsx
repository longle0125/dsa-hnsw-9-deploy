// src/components/LandingPage.jsx
import React from "react";
import { Link } from "react-router-dom";

export default function LandingPage() {
    return (
        <div className="landing-container">
            <h1>Face Recognition Demo</h1>

            <p>Chọn 1 chế độ:</p>

            <div className="btn-group">
                <Link to="/upload">
                    <button className="btn">Nhận diện từ ảnh</button>
                </Link>

                <Link to="/webcam">
                    <button className="btn">Nhận diện real-time webcam</button>
                </Link>
            </div>
        </div>
    );
}
