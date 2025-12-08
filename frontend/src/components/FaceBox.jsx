// src/components/FaceBox.jsx
import React from "react";

const FaceBox = ({ face }) => {
  const imgSrc =
    face.imgSrc ||
    face.crop_image ||
    face.image_url ||
    null;

  const mssv =
    face.mssv ||
    face.student_id ||
    face.info?.MSSV ||
    "Không tìm thấy";

  const name =
    face.name ||
    face.info?.Ten ||
    "Unknown";

  const rawDistance =
    typeof face.distance === "number"
      ? face.distance
      : typeof face.similarity === "number"
      ? face.similarity
      : face.distance;

  const distance =
    typeof rawDistance === "number"
      ? rawDistance.toFixed(3)
      : rawDistance;

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
              className="d-flex align-items-center justify-content-center rounded-start m-2 bg-secondary bg-opacity-25 border border-secondary"
              style={{ width: 80, height: 80, fontSize: 28 }}
            >
              <i className="ti-user" />
            </div>
          )}
        </div>

        <div className="col">
          <div className="card-body py-2 pe-3">
            <p className="mb-1 small text-light">
              <strong>ID:</strong> {mssv}
            </p>
            <p className="mb-1 small text-light">
              <strong>Tên:</strong> {name}
            </p>
            {distance !== undefined && distance !== null && (
              <p className="mb-0 small text-light">
                <strong>Độ tương đồng (distance):</strong> {distance}
              </p>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

export default FaceBox;
