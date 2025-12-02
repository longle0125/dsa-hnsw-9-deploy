import base64
import cv2
import numpy as np
import face_recognition
from flask import Flask, request, jsonify
from flask_cors import CORS

# Nếu file hnsw_manager.py nằm trong thư mục con services/ thì import: from services.search_manager import FaceSearchEngine
# Nếu nằm cùng thư mục thì giữ nguyên:
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
    # [UPDATED] Đổi thông báo port thành 8000
    print("[SUCCESS] Server da san sang phuc vu tai http://127.0.0.1:8000")
except Exception as e:
    print(f"[ERROR] LOI NGHIEM TRONG: Khong the khoi dong HNSW. Chi tiet: {e}")


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


# --- API 1: UPLOAD FILE ẢNH ---
@app.route('/recognize_image', methods=['POST']) 
def search_by_file():
    if 'file' not in request.files:
        return jsonify({"error": "Vui long gui kem file anh (key='file')"}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "Chua chon file"}), 400

    try:
        # Đọc ảnh trực tiếp từ file gửi lên
        image = face_recognition.load_image_file(file)
        
  
        face_locations = face_recognition.face_locations(image, model='hog')
        
        if len(face_locations) == 0:
         
            return jsonify({"faces": []}), 200
            
    
        face_encodings = face_recognition.face_encodings(image, face_locations)
        
        results = []
      
        for i, query_vector in enumerate(face_encodings):
            search_result = search_engine.search_face(query_vector)
            
            top, right, bottom, left = face_locations[i]
            
            # Chuẩn hóa dữ liệu trả về cho khớp với Frontend
            face_data = {
                "student_id": search_result['info'].get('MSSV', 'Unknown') if search_result['status'] == 'found' else 'Unknown',
                "name": search_result['info'].get('Ten', 'Unknown') if search_result['status'] == 'found' else 'Unknown',
                "distance": search_result.get('distance', 0),
                "box": [top, right, bottom, left],
                "crop_image": "" # Có thể thêm logic cắt ảnh base64 nếu muốn hiện crop
            }
            results.append(face_data)
        
        # Trả về đúng format {"faces": [...]} mà Frontend cần
        return jsonify({"faces": results}), 200

    except Exception as e:
        print(f"[ERROR] Loi xu ly file: {e}")
        return jsonify({"error": str(e)}), 500


# --- API 2: NHẬN DIỆN REALTIME (Webcam) ---

@app.route('/recognize_frame', methods=['POST']) 
def search_by_base64():
    data = request.get_json()
    if not data or 'image' not in data:
        return jsonify({"error": "Thieu du lieu 'image'"}), 400

    base64_str = data['image']
    

    image_rgb = decode_base64_image(base64_str)
    if image_rgb is None:
        return jsonify({"error": "Anh base64 loi"}), 400

    try:

        face_locations = face_recognition.face_locations(image_rgb, model='hog')
        
        if len(face_locations) == 0:
   
            return jsonify({"faces": []}), 200


        face_encodings = face_recognition.face_encodings(image_rgb, face_locations)
        
        results = []
        # Xử lý tất cả các khuôn mặt tìm thấy trong khung hình
        for i, face_encoding in enumerate(face_encodings):
            # Gọi HNSW tìm kiếm
            search_result = search_engine.search_face(face_encoding)
            
            top, right, bottom, left = face_locations[i]
            
            # Cấu trúc dữ liệu trả về cho Frontend (khớp với FaceBox.jsx)
            face_data = {
                "student_id": search_result['info'].get('MSSV', 'Unknown') if search_result['status'] == 'found' else 'Unknown',
                "name": search_result['info'].get('Ten', 'Unknown') if search_result['status'] == 'found' else 'Unknown',
                "distance": search_result.get('distance', 0),
                "box": [top, right, bottom, left],
                "crop_image": "" # Frontend đang dùng placeholder, có thể gửi lại base64 crop nếu cần
            }
            results.append(face_data)
        
        return jsonify({"faces": results}), 200

    except Exception as e:
        print(f"[ERROR] Loi realtime: {e}")
        return jsonify({"error": str(e)}), 500

# --- CHẠY APP ---
if __name__ == '__main__':
    # [UPDATED] Chạy ở Port 8000 để khớp với Frontend
    app.run(host='0.0.0.0', port=8000, debug=True)