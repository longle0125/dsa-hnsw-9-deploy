// src/services/api.js
const API_URL = "http://localhost:8000"; // Đổi nếu backend chạy port khác

// Nhận diện qua file ảnh (form-data: key=file)
export async function recognizeImage(formData) {
  const res = await fetch(`${API_URL}/api/recognize_image`, {
    method: "POST",
    body: formData,
  });
  return await res.json();
}

// (optional) Lấy thống kê nếu backend có
export async function getStats() {
  const res = await fetch(`${API_URL}/stats`);
  return await res.json();
}

// Nhận diện 1 frame (Webcam) – body: { image: "data:image/jpeg;base64,..." }
export async function recognizeFrame(base64Image) {
  const res = await fetch(`${API_URL}/api/recognize_frame`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ image: base64Image }),
  });
  return await res.json();
}
