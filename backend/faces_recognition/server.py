import base64
import cv2
import numpy as np
import face_recognition
from flask import Flask, request, jsonify
from flask_cors import CORS
from hnsw_manager import FaceSearchEngine

# ---CẤU HÌNH SERVER ---
app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

# ---KHỞI ĐỘNG HNSW ---
print("[INFO] Dang khoi dong Server va nap du lieu...")
search_engine = FaceSearchEngine()

try:
    # Load dữ liệu từ Mongo và xây cây HNSW ngay khi Server bật
    search_engine.load_data_and_build_index()
    print("[SUCCESS] Server da san sang phuc vu tai http://127.0.0.1:5000")
except Exception as e:
    print(f"[ERROR] LOI NGHIEM TRONG: Khong the khoi dong HNSW. Chi tiet: {e}")


# ---HÀM PHỤ TRỢ: GIẢI MÃ ẢNH BASE64 ---
def decode_base64_image(base64_string):
    """Chuyển chuỗi Base64 từ Webcam thành ảnh OpenCV (RGB)"""
    try:
        if "," in base64_string:
            base64_string = base64_string.split(",")[1]
        
        img_bytes = base64.b64decode(base64_string)
        nparr = np.frombuffer(img_bytes, np.uint8)
        img_bgr = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        img_rgb = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB)
        return img_rgb
    except Exception as e:
        print(f"[ERROR] Loi decode anh: {e}")
        return None


# --- API 1: UPLOAD FILE ẢNH (Test Postman) ---
@app.route('/api/search_file', methods=['POST'])
def search_by_file():
    if 'file' not in request.files:
        return jsonify({"error": "Vui long gui kem file anh (key='file')"}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "Chua chon file"}), 400

    try:
        image = face_recognition.load_image_file(file)
        
        # 1. Tìm vị trí khuôn mặt
        face_locations = face_recognition.face_locations(image)
        
        if len(face_locations) == 0:
            return jsonify({"status": "failed", "message": "Khong tim thay mat nao"}), 200
            
        # 2. Encode khuôn mặt đầu tiên
        face_encodings = face_recognition.face_encodings(image, face_locations)
        query_vector = face_encodings[0]
        
        # 3. Gọi HNSW để tìm
        result = search_engine.search_face(query_vector)
        
        return jsonify(result), 200

    except Exception as e:
        print(f"[ERROR] Loi xu ly file: {e}")
        return jsonify({"error": str(e)}), 500


# --- 5. API 2: NHẬN DIỆN REALTIME (Webcam) ---
@app.route('/api/search_base64', methods=['POST'])
def search_by_base64():
    data = request.get_json()
    if not data or 'image' not in data:
        return jsonify({"error": "Thieu du lieu 'image'"}), 400

    base64_str = data['image']
    
    image_rgb = decode_base64_image(base64_str)
    if image_rgb is None:
        return jsonify({"error": "Anh base64 loi"}), 400

    try:
        # Dùng model='hog' cho nhanh với CPU
        face_locations = face_recognition.face_locations(image_rgb, model='hog')
        
        if len(face_locations) == 0:
            return jsonify({"status": "failed", "message": "No face"}), 200

        face_encodings = face_recognition.face_encodings(image_rgb, face_locations)
        query_vector = face_encodings[0]

        # Gọi HNSW tìm kiếm
        result = search_engine.search_face(query_vector)
        
        # Trả thêm tọa độ để vẽ khung
        top, right, bottom, left = face_locations[0]
        result['box'] = {"top": top, "right": right, "bottom": bottom, "left": left}
        
        return jsonify(result), 200

    except Exception as e:
        print(f"[ERROR] Loi realtime: {e}")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)