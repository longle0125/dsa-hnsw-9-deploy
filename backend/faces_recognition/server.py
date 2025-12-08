import base64
import time
import cv2
import numpy as np
import face_recognition
from flask import Flask, request, jsonify
from flask_cors import CORS
from io import BytesIO
from PIL import Image

from hnsw_manager import FaceSearchEngine

# --- CẤU HÌNH SERVER ---
app = Flask(__name__)
# Cho phép Frontend từ mọi nguồn (localhost, deploy) gọi vào
CORS(app, resources={r"/*": {"origins": "*"}})

# --- KHỞI ĐỘNG HNSW ---
print("[INFO] Dang khoi dong Server va nap du lieu...")
search_engine = FaceSearchEngine()

try:
    # Load dữ liệu từ Mongo và xây cây HNSW ngay khi Server bật
    search_engine.load_data_and_build_index()
    print("[SUCCESS] Server da san sang phuc vu tai http://localhost:8000")
except Exception as e:
    print(f"[ERROR] LOI NGHIEM TRONG: Khong the khoi dong HNSW. Chi tiet: {e}")


# ----------------- HÀM BRUTE-FORCE -----------------
def brute_force_search(query_vector, threshold=0.5):
    """
    Tìm kiếm brute-force trên MongoDB:
    - Duyệt tất cả feature_vector
    - Tính khoảng cách L2
    - Lấy doc có distance nhỏ nhất
    """
    collection = search_engine.collection  # đã cấu hình sẵn trong FaceSearchEngine
    cursor = collection.find({"feature_vector": {"$exists": True}})

    best_doc = None
    best_dist = None

    q = np.array(query_vector, dtype=np.float32)

    for doc in cursor:
        vec = doc.get("feature_vector")
        if not isinstance(vec, list):
            continue

        v = np.array(vec, dtype=np.float32)
        if v.shape[0] != q.shape[0]:
            continue

        d = np.linalg.norm(q - v)

        if best_dist is None or d < best_dist:
            best_dist = d
            best_doc = doc

    if best_doc is None or best_dist is None:
        return {"status": "unknown", "distance": None, "info": {}}

    status = "found" if best_dist <= threshold else "unknown"

    info = {
        "MSSV": best_doc.get("MSSV", "Unknown"),
        "Ten": best_doc.get("Ten", "Unknown"),
    }

    return {
        "status": status,
        "distance": float(best_dist),
        "info": info,
    }


# --- HÀM PHỤ TRỢ: GIẢI MÃ ẢNH BASE64 ---
def decode_base64_image(base64_string):
    """Chuyển chuỗi Base64 từ Webcam thành ảnh OpenCV (RGB)"""
    try:
        # Nếu chuỗi có header (ví dụ: "data:image/jpeg;base64,..."), hãy cắt bỏ nó
        if "," in base64_string:
            base64_string = base64_string.split(",")[1]

        img_bytes = base64.b64decode(base64_string)
        nparr = np.frombuffer(img_bytes, np.uint8)
        img_bgr = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

        # Quan trọng: OpenCV dùng BGR, face_recognition cần RGB
        img_rgb = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB)
        return img_rgb
    except Exception as e:
        print(f"[ERROR] Loi decode anh: {e}")
        return None


# --- HÀM PHỤ TRỢ: CẮT ẢNH KHUÔN MẶT RA BASE64 ---
def crop_face_to_base64(image_rgb, top, right, bottom, left):
    try:
        # Cắt ảnh theo toạ độ [y:y+h, x:x+w]
        face_image = image_rgb[top:bottom, left:right]

        # Chuyển sang PIL Image
        pil_img = Image.fromarray(face_image)

        # Lưu vào buffer
        buffered = BytesIO()
        pil_img.save(buffered, format="JPEG")

        # Encode base64
        img_str = base64.b64encode(buffered.getvalue()).decode("utf-8")
        return f"data:image/jpeg;base64,{img_str}"
    except Exception as e:
        print(f"[ERROR] Loi crop anh: {e}")
        return ""


# --- API 1: UPLOAD FILE ẢNH ---
# Gọi từ frontend: POST /recognize_image?mode=hnsw|bruteforce
@app.route("/recognize_image", methods=["POST"])
def search_by_file():
    start_time = time.time()

    mode = request.args.get("mode", "hnsw").lower()
    if mode not in {"hnsw", "bruteforce"}:
        mode = "hnsw"

    if "file" not in request.files:
        return jsonify({"error": "Vui long gui kem file anh (key='file')"}), 400

    file = request.files["file"]
    if file.filename == "":
        return jsonify({"error": "Chua chon file"}), 400

    try:
        # Đọc ảnh trực tiếp từ file gửi lên
        image = face_recognition.load_image_file(file)

        # 1. Tìm vị trí khuôn mặt (Dùng HOG cho nhanh)
        face_locations = face_recognition.face_locations(image, model="hog")

        if len(face_locations) == 0:
            elapsed_ms = (time.time() - start_time) * 1000
            return jsonify({"faces": [], "mode": mode, "elapsed_ms": elapsed_ms}), 200

        # 2. Encode khuôn mặt
        face_encodings = face_recognition.face_encodings(image, face_locations)

        results = []

        # 3. Duyệt qua từng mặt tìm thấy
        for i, query_vector in enumerate(face_encodings):
            # Chọn thuật toán
            if mode == "bruteforce":
                search_result = brute_force_search(query_vector)
            else:
                search_result = search_engine.search_face(query_vector)

            if not search_result:
                continue

            top, right, bottom, left = face_locations[i]

            # Cắt ảnh khuôn mặt
            crop_b64 = crop_face_to_base64(image, top, right, bottom, left)

            face_data = {
                "student_id": search_result.get("info", {}).get(
                    "MSSV", "Unknown"
                )
                if search_result.get("status") == "found"
                else "Unknown",
                "name": search_result.get("info", {}).get(
                    "Ten", "Unknown"
                )
                if search_result.get("status") == "found"
                else "Unknown",
                "distance": search_result.get("distance", 0),
                "box": [top, right, bottom, left],
                "crop_image": crop_b64,
                "mode": mode,
            }
            results.append(face_data)

        elapsed_ms = (time.time() - start_time) * 1000
        return jsonify({"faces": results, "mode": mode, "elapsed_ms": elapsed_ms}), 200

    except Exception as e:
        print(f"[ERROR] Loi xu ly file: {e}")
        return jsonify({"error": str(e)}), 500


# --- API 2: NHẬN DIỆN REALTIME (WEBCAM) ---
# Gọi từ frontend: POST /recognize_frame?mode=hnsw|bruteforce
@app.route("/recognize_frame", methods=["POST"])
def search_by_base64():
    start_time = time.time()

    mode = request.args.get("mode", "hnsw").lower()
    if mode not in {"hnsw", "bruteforce"}:
        mode = "hnsw"

    # 1. Lấy dữ liệu JSON
    data = request.get_json()
    if not data or "image" not in data:
        return jsonify({"error": "Thieu du lieu 'image'"}), 400

    base64_str = data["image"]

    # 2. Giải mã Base64 -> Ảnh RGB
    image_rgb = decode_base64_image(base64_str)
    if image_rgb is None:
        return jsonify({"error": "Anh base64 loi"}), 400

    try:
        # 3. Tìm vị trí mặt (HOG)
        face_locations = face_recognition.face_locations(image_rgb, model="hog")

        if len(face_locations) == 0:
            elapsed_ms = (time.time() - start_time) * 1000
            return jsonify({"faces": [], "mode": mode, "elapsed_ms": elapsed_ms}), 200

        # 4. Encode mặt (Trích xuất đặc trưng 128D)
        face_encodings = face_recognition.face_encodings(image_rgb, face_locations)

        results = []

        # 5. Duyệt và tìm kiếm
        for i, face_encoding in enumerate(face_encodings):
            # Chọn thuật toán
            if mode == "bruteforce":
                search_result = brute_force_search(face_encoding)
            else:
                search_result = search_engine.search_face(face_encoding)

            if not search_result:
                continue

            top, right, bottom, left = face_locations[i]
            crop_b64 = crop_face_to_base64(image_rgb, top, right, bottom, left)

            face_data = {
                "student_id": search_result.get("info", {}).get(
                    "MSSV", "Unknown"
                )
                if search_result.get("status") == "found"
                else "Unknown",
                "name": search_result.get("info", {}).get(
                    "Ten", "Unknown"
                )
                if search_result.get("status") == "found"
                else "Unknown",
                "distance": search_result.get("distance", 0),
                "box": [top, right, bottom, left],
                "crop_image": crop_b64,
                "mode": mode,
            }
            results.append(face_data)

        elapsed_ms = (time.time() - start_time) * 1000
        return jsonify({"faces": results, "mode": mode, "elapsed_ms": elapsed_ms}), 200

    except Exception as e:
        print(f"[ERROR] Loi realtime: {e}")
        return jsonify({"error": str(e)}), 500


# --- CHẠY APP ---
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
