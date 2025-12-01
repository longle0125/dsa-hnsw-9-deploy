// src/components/WebcamPage.jsx
import React, { useEffect, useRef, useState } from "react";
import { recognizeFrame } from "../services/api";
import FaceBox from "../components/FaceBox";

export default function WebcamPage() {
    const videoRef = useRef(null);
    const canvasRef = useRef(null);
    const [results, setResults] = useState([]);

    useEffect(() => {
        async function initCamera() {
            const stream = await navigator.mediaDevices.getUserMedia({ video: true });
            videoRef.current.srcObject = stream;
        }
        initCamera();
    }, []);

    async function captureFrame() {
        const video = videoRef.current;
        const canvas = canvasRef.current;
        const ctx = canvas.getContext("2d");

        canvas.width = video.videoWidth;
        canvas.height = video.videoHeight;

        ctx.drawImage(video, 0, 0, canvas.width, canvas.height);

        const base64Image = canvas.toDataURL("image/jpeg");

        const res = await recognizeFrame(base64Image);
        setResults(res.faces);
    }

    useEffect(() => {
        const interval = setInterval(captureFrame, 800); // 0.8s mỗi frame
        return () => clearInterval(interval);
    }, []);

    return (
        <div>
            <h2>Nhận diện Webcam Real-time</h2>

            <video ref={videoRef} autoPlay style={{ width: "500px" }}></video>

            <canvas ref={canvasRef} style={{ display: "none" }}></canvas>

            <div className="results">
                {results.map((face, index) => (
                    <FaceBox key={index} face={face} />
                ))}
            </div>
        </div>
    );
}
