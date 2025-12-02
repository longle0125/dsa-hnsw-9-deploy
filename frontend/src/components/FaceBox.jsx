import React from "react";

const FaceBox = ({ face }) => {
  // backend có thể trả crop_image hoặc image_url
  const imgSrc = face.crop_image || face.image_url || null;
  const mssv = face.student_id || face.mssv || "Không tìm thấy";
  const name = face.name || "Unknown";
  const distance =
    typeof face.distance === "number"
      ? face.distance.toFixed(3)
      : face.distance;

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
            <p className="mb-1 small">
              <strong>id:</strong> {mssv}
            </p>
            <p className="mb-1 small">
              <strong>Tên:</strong> {name}
            </p>
            {distance !== undefined && (
              <p className="mb-0 small">
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
