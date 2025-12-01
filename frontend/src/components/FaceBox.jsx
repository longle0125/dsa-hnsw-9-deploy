// src/components/FaceBox.jsx
import React from "react";

export default function FaceBox({ face }) {
    return (
        <div className="face-box">
            <img src={face.crop_image} alt="face" />

            <div className="info">
                <p><strong>MSSV:</strong> {face.student_id ?? "Không tìm thấy"}</p>
                <p><strong>Tên:</strong> {face.name ?? "Unknown"}</p>
                <p><strong>Độ tin cậy:</strong> {face.distance?.toFixed(3)}</p>
            </div>
        </div>
    );
}
