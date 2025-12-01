// src/pages/LandingPage.jsx
import React from "react";
import { Link } from "react-router-dom";

import logoImg from "../assets/logo_dark_cyan.png";

const LandingPage = () => {
  const year = new Date().getFullYear();

  return (
    <div className="d-flex flex-column min-vh-100 bg-dark text-light">
      {/* Main content */}
      <main className="flex-grow-1 py-5">
        <div className="container">
          {/* Hero */}
          <section className="text-center mb-5">
            <h1 className="display-6 fw-bold mb-2">
              Chào mừng đến với {" "}
              <span className="text-primary">FaceReco</span>
            </h1>
            <p className="mx-auto" style={{ maxWidth: 600, opacity: 0.5 }}>
              Hệ thống nhận diện khuôn mặt theo thời gian thực từ camera hoặc ảnh
              tải lên, sử dụng thuật toán <strong>HNSW</strong> cho tìm kiếm
              vector nhanh trên cơ sở dữ liệu sinh viên.
            </p>
          </section>

          {/* Mode cards */}
          <section className="row g-4 justify-content-center">
            {/* Live Cam */}
            <div className="col-md-6">
              <div className="mode-card h-100 p-4">
                <div className="d-flex align-items-center mb-3 gap-3">
                  <div className="mode-icon-circle bg-primary bg-opacity-25 border border-primary border-opacity-50 text-primary">
                    <i className="ti-video-camera" />
                  </div>
                  <div>
                    <h2 className="text-primary h5 mb-1">
                      Chế độ Webcam
                    </h2>
                    <p
                      className="text-light small mb-0"
                      style={{ opacity: 0.5 }}
                    >
                      Nhận diện khuôn mặt trực tiếp từ camera trình duyệt.
                    </p>
                  </div>
                </div>

                <p
                  className="text-light small mb-3"
                  style={{ opacity: 0.8 }}
                >
                  Sử dụng camera đang kết nối để liên tục phát hiện và nhận diện
                  khuôn mặt, kết hợp tìm kiếm vector bằng HNSW với độ trễ thấp.
                </p>

                <ul
                  className="text-light small mb-4 ps-3"
                  style={{ opacity: 0.8 }}
                >
                  <li>Streaming khung hình trực tiếp từ webcam.</li>
                  <li>Hiển thị bounding box và nhãn tên sinh viên.</li>
                  <li>
                    Tìm kiếm láng giềng gần nhất bằng HNSW trên không gian
                    embedding.
                  </li>
                </ul>

                <Link
                  to="/webcam"
                  className="btn btn-primary rounded-pill text-dark fw-semibold text-decoration-none"
                >
                  <i className="ti-control-play me-1" />
                  Webcam
                </Link>
              </div>
            </div>

            {/* Upload */}
            <div className="col-md-6">
              <div className="mode-card h-100 p-4">
                <div className="d-flex align-items-center mb-3 gap-3">
                  <div className="mode-icon-circle bg-info bg-opacity-25 border border-info border-opacity-50 text-info">
                    <i className="ti-upload" />
                  </div>
                  <div>
                    <h2 className="text-info h5 mb-1">
                      Chế độ Upload
                    </h2>
                    <p
                      className="text-light small mb-0"
                      style={{ opacity: 0.5 }}
                    >
                      Phân tích ảnh tĩnh chứa một hoặc nhiều khuôn mặt.
                    </p>
                  </div>
                </div>

                <p
                  className="text-light small mb-3"
                  style={{ opacity: 0.8 }}
                >
                  Tải lên ảnh chụp để hệ thống phát hiện tất cả khuôn mặt xuất
                  hiện, ánh xạ tới thông tin sinh viên tương ứng và hiển thị độ
                  tương đồng.
                </p>

                <ul
                  className="text-light small mb-4 ps-3"
                  style={{ opacity: 0.8 }}
                >
                  <li>Hỗ trợ nhiều khuôn mặt trong một ảnh.</li>
                  <li>Hiển thị MSSV, họ tên và distance (độ tương đồng).</li>
                  <li>Thông báo rõ ràng khi không tìm thấy sinh viên phù hợp.</li>
                </ul>

                <Link
                  to="/upload"
                  className="btn btn-info rounded-pill text-dark fw-semibold text-decoration-none"
                >
                  <i className="ti-arrow-up me-1" />
                  Upload
                </Link>
              </div>
            </div>
          </section>
        </div>
      </main>

      {/* Footer */}
      <footer
        className="border-top border-secondary py-3 text-center text-light small"
        style={{ opacity: 0.5 }}
      >
        © {year} FaceReco Project · Xây dựng bằng Python, React, Bootstrap 5 &amp; HNSW
      </footer>
    </div>
  );
};

export default LandingPage;
