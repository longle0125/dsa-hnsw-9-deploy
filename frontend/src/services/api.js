// src/services/api.js
const API_BASE = "http://localhost:8000"; // chỉnh lại nếu bạn dùng port khác

function getSearchMode() {
  const mode = window.localStorage.getItem("searchMode");
  // fallback mặc định là HNSW
  return mode === "bruteforce" ? "bruteforce" : "hnsw";
}

export async function recognizeImage(formData) {
  const mode = getSearchMode();

  const res = await fetch(`${API_BASE}/recognize_image?mode=${mode}`, {
    method: "POST",
    body: formData,
  });

  if (!res.ok) {
    throw new Error("Upload API error");
  }

  const data = await res.json();
  // Gắn thêm thông tin thời gian client-side (nếu muốn)
  return data;
}

export async function recognizeFrame(base64Image) {
  const mode = getSearchMode();

  const payload = { image: base64Image };

  const res = await fetch(`${API_BASE}/recognize_frame?mode=${mode}`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(payload),
  });

  if (!res.ok) {
    throw new Error("Webcam API error");
  }

  const data = await res.json();
  return data;
}
