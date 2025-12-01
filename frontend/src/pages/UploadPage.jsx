// src/components/UploadPage.jsx
import React, { useState } from "react";
import { recognizeImage } from "../services/api";
import FaceBox from "../components/FaceBox";

export default function UploadPage() {
    const [imageFile, setImageFile] = useState(null);
    const [results, setResults] = useState([]);

    async function handleUpload() {
        if (!imageFile) return;

        const formData = new FormData();
        formData.append("file", imageFile);

        const res = await recognizeImage(formData);
        setResults(res.faces);
    }

    return (
        <div>
            <h2>Nhận diện từ ảnh</h2>

            <input
                type="file"
                accept="image/*"
                onChange={(e) => setImageFile(e.target.files[0])}
            />

            <button onClick={handleUpload}>Nhận diện</button>

            <div className="results">
                {results.map((face, index) => (
                    <FaceBox key={index} face={face} />
                ))}
            </div>
        </div>
    );
}
