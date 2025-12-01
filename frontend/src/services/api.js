// src/services/api.js
const API_URL = "http://localhost:8000"; // đổi lại khi deploy

// Upload ảnh để nhận diện
export async function recognizeImage(formData) {
    const res = await fetch(`${API_URL}/recognize_image`, {
        method: "POST",
        body: formData
    });
    return await res.json();
}

// Lấy danh sách vector đã index (optional)
export async function getStats() {
    const res = await fetch(`${API_URL}/stats`);
    return await res.json();
}

// Nhận diện 1 frame (cho webcam)
export async function recognizeFrame(base64Image) {
    const res = await fetch(`${API_URL}/recognize_frame`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ image: base64Image })
    });
    return await res.json();
}
