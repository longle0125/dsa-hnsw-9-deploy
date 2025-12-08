// src/pages/WebcamPage.jsx
import React, { useEffect, useRef, useState } from "react";
import { recognizeFrame } from "../services/api";
import FaceBox from "../components/FaceBox";

const WebcamPage = () => {
  const videoRef = useRef(null);
  const canvasRef = useRef(null);
  const [results, setResults] = useState([]);
  const [running, setRunning] = useState(true);

  // Khởi tạo webcam
  useEffect(() => {
    async function initCamera() {
      try {
        const stream = await navigator.mediaDevices.getUserMedia({
          video: true,
        });
        if (videoRef.current) {
          videoRef.current.srcObject = stream;
        }
      } catch (err) {
        console.error(err);
        alert("Không truy cập được webcam. Hãy kiểm tra quyền truy cập.");
      }
    }

    initCamera();

    // Tắt webcam khi rời trang
    return () => {
      const video = videoRef.current;
      if (video && video.srcObject) {
        video.srcObject.getTracks().forEach((t) => t.stop());
      }
    };
  }, []);

  // Gửi frame định kỳ lên backend
  useEffect(() => {
    if (!running) return;

    const interval = setInterval(captureFrame, 800); // 0.8s/frame cho đỡ nặng
    return () => clearInterval(interval);

    async function captureFrame() {
      const video = videoRef.current;
      const canvas = canvasRef.current;
      if (!video || !canvas || video.readyState !== 4) return;

      const ctx = canvas.getContext("2d");

      // Kích thước canvas = kích thước video
      canvas.width = video.videoWidth;
      canvas.height = video.videoHeight;

      // Vẽ frame hiện tại lên canvas
      ctx.drawImage(video, 0, 0, canvas.width, canvas.height);

      // Convert frame → base64
      const base64Image = canvas.toDataURL("image/jpeg");

      try {
        const res = await recognizeFrame(base64Image);

        // Chuẩn hoá dữ liệu khuôn mặt
        let rawFaces = [];

        if (Array.isArray(res?.faces)) {
          rawFaces = res.faces;
        } else if (res && (res.box || res.info || res.status)) {
          rawFaces = [res];
        }

        const processedFaces = rawFaces.map((face) => {
          const info = face.info || {};

          const mssv =
            face.mssv ||
            face.student_id ||
            info.MSSV ||
            undefined;

          const name =
            face.name ||
            info.Ten ||
            undefined;

          const distance =
            typeof face.distance === "number"
              ? face.distance
              : typeof res?.distance === "number"
              ? res.distance
              : face.distance;

          let imgSrc = face.imgSrc || face.crop_image || face.image_url || null;

          // Nếu chưa có imgSrc mà có box → crop từ canvas
          if (!imgSrc && Array.isArray(face.box)) {
            const [top, right, bottom, left] = face.box;
            const width = right - left;
            const height = bottom - top;

            if (width > 0 && height > 0) {
              const cropCanvas = document.createElement("canvas");
              const cropCtx = cropCanvas.getContext("2d");
              cropCanvas.width = width;
              cropCanvas.height = height;

              cropCtx.drawImage(
                canvas,
                left,
                top,
                width,
                height,
                0,
                0,
                width,
                height
              );

              imgSrc = cropCanvas.toDataURL("image/jpeg");
            }
          }

          return {
            ...face,
            info,
            mssv,
            name,
            distance,
            imgSrc,
          };
        });

        setResults(processedFaces);

        // Vẽ lại frame + khung
        ctx.drawImage(video, 0, 0, canvas.width, canvas.height);
        ctx.strokeStyle = "#0d6efd";
        ctx.lineWidth = 2;
        ctx.font = "12px system-ui";
        ctx.textBaseline = "top";

        processedFaces.forEach((face) => {
          if (!Array.isArray(face.box)) return;
          const [top, right, bottom, left] = face.box;
          const width = right - left;
          const height = bottom - top;

          // Vẽ khung
          ctx.strokeRect(left, top, width, height);

          const displayName = face.name || face.info?.Ten || "Unknown";
          const displayMssv =
            face.mssv || face.student_id || face.info?.MSSV || "";

          const label =
            displayName +
            (displayMssv ? ` (${displayMssv})` : "");

          const textX = left;
          const textY = top - 18 < 0 ? top + 2 : top - 18;

          const textWidth = ctx.measureText(label).width + 6;
          const textHeight = 16;

          ctx.fillStyle = "rgba(0,0,0,0.6)";
          ctx.fillRect(textX, textY, textWidth, textHeight);

          ctx.fillStyle = "#ffffff";
          ctx.fillText(label, textX + 3, textY + 2);
        });
      } catch (err) {
        console.error(err);
      }
    }
  }, [running]);

  return (
    <div className="d-flex flex-column min-vh-90 bg-dark text-light">
      <main className="flex-grow-1 py-3">
        <div className="container">
          <div className="mb-4">
            <h2 className="h4 mb-1 text-light">Chế độ Camera trực tiếp</h2>
            <p className="small text-light mb-0" style={{ opacity: 0.8 }}>
              Hệ thống sẽ chụp khung hình định kỳ từ webcam và gửi lên backend
              để nhận diện khuôn mặt theo thời gian thực.
            </p>
          </div>

          <div className="row g-4">
            {/* Khung webcam – TĂNG LÊN col-lg-8 */}
            <div className="col-lg-8">
              <div className="card bg-dark border-secondary">
                <div className="card-body">
                  <h5 className="card-title mb-3 text-light">Live Camera</h5>

                  <div className="mb-3 text-center position-relative">
                    <video
                      ref={videoRef}
                      autoPlay
                      style={{ display: "none" }}
                    />

                    <canvas
                      ref={canvasRef}
                      className="border border-secondary rounded w-100"
                      style={{
                        height: "480px",
                        maxHeight: "70vh",
                        backgroundColor: "#000",
                      }}
                    />
                  </div>

                  <div className="d-flex gap-2">
                    <button
                      type="button"
                      className={`btn btn-sm rounded-pill ${
                        running ? "btn-outline-warning" : "btn-success"
                      }`}
                      onClick={() => setRunning((prev) => !prev)}
                    >
                      {running ? "Tạm dừng gửi frame" : "Tiếp tục nhận diện"}
                    </button>
                  </div>

                  <p
                    className="small mt-2 mb-0 text-light"
                    style={{ opacity: 0.6 }}
                  >
                    * Khoảng mỗi 0.8 giây sẽ gửi một frame lên server. Tốc độ
                    thực tế phụ thuộc cấu hình backend và mạng.
                  </p>
                </div>
              </div>
            </div>

            {/* Kết quả FaceBox – GIẢM còn col-lg-4 */}
            <div className="col-lg-4">
              <div className="d-flex justify-content-between align-items-center mb-2">
                <h5 className="mb-0 text-light">Kết quả hiện tại</h5>
                <span className="small text-light" style={{ opacity: 0.7 }}>
                  {results.length > 0
                    ? `${results.length} khuôn mặt trong khung hình`
                    : "Chưa có khuôn mặt nào"}
                </span>
              </div>

              {results.length === 0 && (
                <div className="alert alert-secondary py-2 small mb-3">
                  Chưa nhận diện được khuôn mặt nào. Hãy nhìn thẳng vào camera,
                  đứng gần hơn và đảm bảo ánh sáng đủ rõ.
                </div>
              )}

              <div className="row g-3">
                {results.map((face, index) => (
                  <div key={index} className="col-12">
                    <FaceBox face={face} />
                  </div>
                ))}
              </div>
            </div>
          </div>
        </div>
      </main>
    </div>
  );
};

export default WebcamPage;
