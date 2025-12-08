// src/components/FaceBox.jsx
import React from "react";

// Hàm helper: convert distance -> similarity %
function distanceToSimilarity(distance, maxDistance = 0.5) {
  if (typeof distance !== "number" || Number.isNaN(distance)) {
    return 0;
  }

  // similarity = 1 - d / d_max  (clamp 0..1)
  const score = 1 - distance / maxDistance;
  const clamped = Math.max(0, Math.min(1, score));
  return Math.round(clamped * 100); // trả về % nguyên, ví dụ 87
}

const FaceBox = ({ face }) => {
  // Ảnh mặt cắt ra từ backend (upload / webcam)
  const imgSrc = face.crop_image || face.image_url || face.imgSrc || null;

  // Lấy distance “thật”
  let rawDistance;
  if (typeof face.distance === "number") {
    rawDistance = face.distance;
  } else if (typeof face.distance === "string") {
    const parsed = Number(face.distance);
    rawDistance = Number.isNaN(parsed) ? undefined : parsed;
  }

  const similarity = distanceToSimilarity(rawDistance); // 0–100 (%)

  // Lấy MSSV / Tên từ backend nếu có
  let mssv =
    face.student_id ||
    face.mssv ||
    face.info?.MSSV ||
    "Không tìm thấy";

  let name =
    face.name ||
    face.info?.Ten ||
    "Unknown";

  // ❗ Nếu độ tương đồng = 0% → coi như không nhận ra
  if (similarity === 0) {
    mssv = "Unknown";
    name = "Unknown";
  }

  const distanceText =
    typeof rawDistance === "number" && !Number.isNaN(rawDistance)
      ? rawDistance.toFixed(3)
      : undefined;

  return (
    <div className="card bg-dark border-secondary h-100">
      <div className="row g-0 align-items-center">
        <div className="col-auto">
          {imgSrc ? (
            <img
              src={imgSrc}
              alt="face"
              className="img-fluid rounded-start m-2 border border-secondary"
              style={{ width: 80, height: 80, objectFit: "cover" }}
            />
          ) : (
            <div
              className="d-flex align-items-center justify-content-center rounded-start m-2 bg-secondary bg-opacity-25 border border-secondary text-muted"
              style={{ width: 80, height: 80, fontSize: 28 }}
            >
              <i className="ti-user" />
            </div>
          )}
        </div>

        <div className="col">
          <div className="card-body py-2 pe-3">
            <p className="mb-1 small text-light" style={{ opacity: 0.8 }}>
              <strong>ID:</strong> {mssv}
            </p>
            <p className="mb-1 small text-light" style={{ opacity: 0.8 }}>
              <strong>Tên:</strong> {name}
            </p>

            {/* Hiển thị độ tương đồng */}
            {similarity !== undefined && (
              <p className="mb-1 small text-light" style={{ opacity: 0.8 }}>
                <strong>Độ tương đồng:</strong> {similarity}%
              </p>
            )}

            {/* Optional: vẫn hiển thị distance để debug */}
            {distanceText && (
              <p className="mb-0 small text-light" style={{ opacity: 0.8 }}>
                <strong>Distance:</strong> {distanceText}
              </p>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

export default FaceBox;
