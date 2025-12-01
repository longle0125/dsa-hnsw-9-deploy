// src/pages/AboutPage.jsx
import React from "react";

const AboutPage = () => {
  const year = new Date().getFullYear();

  return (
    <div className="container py-4">
      {/* Title */}
      <div className="mb-4">
        <h1 className="h3 mb-2">About this project</h1>
        <p className="text-light small mb-0" style={{ opacity: 0.8 }}>
          Face Recognition System with HNSW Search – course project for{" "}
          <strong>Data Structures &amp; Algorithms (DSA) – Honors Program</strong>.
        </p>
      </div>

      {/* Overview card */}
      <div className="card bg-dark border-secondary mb-4">
        <div className="card-body">
          <h5 className="card-title text-light mb-3">
            <i className="ti-info-alt me-2" />
            Giới thiệu
          </h5>
          <p className="card-text small text-light mb-3" style={{ opacity: 0.8 }}>
            Hệ thống nhận diện khuôn mặt thời gian thực, kết hợp{" "}
            <strong>Face Recognition</strong> để trích xuất vector đặc trưng
            khuôn mặt và <strong>HNSW (Hierarchical Navigable Small World)</strong>{" "}
            để tìm kiếm láng giềng gần nhất với độ trễ thấp trên tập dữ liệu lớn.
          </p>

          <div className="d-flex flex-wrap gap-2 small">
            <span className="badge bg-primary">
              <i className="ti-loop me-1" />
              HNSW vector search
            </span>
            <span className="badge bg-success">
              <i className="ti-face-smile me-1" />
              Real-time identification
            </span>
            <span className="badge bg-info text-dark">
              <i className="ti-desktop me-1" />
              Web UI (upload &amp; webcam)
            </span>
            <span className="badge bg-secondary">
              <i className="ti-harddrives me-1" />
              MongoDB metadata
            </span>
          </div>
        </div>
      </div>

      {/* Features + flow */}
      <div className="row g-4 mb-4">
        <div className="col-md-6">
          <div className="card bg-dark border-secondary h-100">
            <div className="card-body">
              <h5 className="card-title text-light mb-3">
                <i className="ti-bolt me-2" />
                Tính năng chính
              </h5>
              <ul className="small text-light mb-0 ps-3" style={{ opacity: 0.8 }}>
                <li>Nhận diện khuôn mặt từ ảnh upload hoặc webcam.</li>
                <li>
                  Mã hóa khuôn mặt thành vector đặc trưng và lưu kèm metadata
                  trong MongoDB.
                </li>
                <li>
                  Sử dụng HNSW để truy vấn vector gần nhất, nhanh hơn brute‑force.
                </li>
                <li>Trả về MSSV, tên và độ tương đồng (distance / confidence).</li>
              </ul>
            </div>
          </div>
        </div>

        <div className="col-md-6">
          <div className="card bg-dark border-secondary h-100">
            <div className="card-body">
              <h5 className="card-title text-light mb-3">
                <i className="ti-direction-alt me-2" />
                Luồng xử lý
              </h5>
              <ol className="small text-light mb-0 ps-3" style={{ opacity: 0.8 }}>
                <li>Client gửi ảnh (file hoặc base64 từ webcam) lên backend.</li>
                <li>Backend trích xuất khuôn mặt và sinh vector embedding.</li>
                <li>HNSW index tìm vector gần nhất trong bộ dữ liệu.</li>
                <li>
                  Backend lấy thông tin sinh viên (MSSV, tên, v.v.) từ MongoDB và
                  trả kết quả JSON về cho client.
                </li>
              </ol>
            </div>
          </div>
        </div>
      </div>

      {/* Team table */}
      <div className="card bg-dark border-secondary mb-4">
        <div className="card-body">
          <h5 className="card-title text-light mb-3">
            <i className="ti-user me-2" />
            Nhóm thực hiện
          </h5>
          <div className="table-responsive">
            <table className="table table-dark table-sm align-middle mb-0">
              <thead>
                <tr>
                  <th>Tên</th>
                  <th>MSSV</th>
                  <th>Vai trò</th>
                </tr>
              </thead>
              <tbody>
                <tr>
                  <td>Lê Hoàng Long</td>
                  <td>2411915</td>
                  <td>Backend – HNSW &amp; API</td>
                </tr>
                <tr>
                  <td>Nguyễn Tiến Đạt</td>
                  <td>2410712</td>
                  <td>Frontend – Web UI</td>
                </tr>
                <tr>
                  <td>Nguyễn Hoàng Minh</td>
                  <td>2412084</td>
                  <td>Data – Pipeline &amp; MongoDB</td>
                </tr>
              </tbody>
            </table>
          </div>
          <p className="text-light small mt-2 mb-0" style={{ opacity: 0.8 }}>
            Dự án thuộc môn <strong>Data Structures &amp; Algorithms</strong> –
            Chương trình Tài năng (Honors Program).
          </p>
        </div>
      </div>
    </div>
  );
};

export default AboutPage;
