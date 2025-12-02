import base64
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
        
        # 1. Tìm vị trí khuôn mặt (Dùng HOG cho nhanh)
        face_locations = face_recognition.face_locations(image, model='hog')
        
        if len(face_locations) == 0:
            return jsonify({"faces": []}), 200
            
        # 2. Encode khuôn mặt
        face_encodings = face_recognition.face_encodings(image, face_locations)
        
        results = []
        
        # 3. Duyệt qua từng mặt tìm thấy
        for i, query_vector in enumerate(face_encodings):
            search_result = search_engine.search_face(query_vector)
            
            if not search_result:
                continue

            top, right, bottom, left = face_locations[i]
            
            # Cắt ảnh khuôn mặt
            crop_b64 = crop_face_to_base64(image, top, right, bottom, left)

            face_data = {
                "student_id": search_result['info'].get('MSSV', 'Unknown') if search_result['status'] == 'found' else 'Unknown',
                "name": search_result['info'].get('Ten', 'Unknown') if search_result['status'] == 'found' else 'Unknown',
                "distance": search_result.get('distance', 0),
                "box": [top, right, bottom, left],
                "crop_image": crop_b64 
            }
            results.append(face_data)
        
        return jsonify({"faces": results}), 200

    except Exception as e:
        print(f"[ERROR] Loi xu ly file: {e}")
        return jsonify({"error": str(e)}), 500


# --- API 2: NHẬN DIỆN REALTIME (WEBCAM) ---
@app.route('/recognize_frame', methods=['POST']) 
def search_by_base64():
    # 1. Lấy dữ liệu JSON
    data = request.get_json()
    if not data or 'image' not in data:
        return jsonify({"error": "Thieu du lieu 'image'"}), 400

    base64_str = data['image']
    
    # 2. Giải mã Base64 -> Ảnh RGB
    image_rgb = decode_base64_image(base64_str)
    if image_rgb is None:
        return jsonify({"error": "Anh base64 loi"}), 400

    try:
        # 3. Tìm vị trí mặt (HOG)
        face_locations = face_recognition.face_locations(image_rgb, model='hog')
        
        if len(face_locations) == 0:
            return jsonify({"faces": []}), 200

        # 4. Encode mặt (Trích xuất đặc trưng 128D)
        face_encodings = face_recognition.face_encodings(image_rgb, face_locations)
        
        results = []
        
        # 5. Duyệt và tìm kiếm
        for i, face_encoding in enumerate(face_encodings):
            # Gọi HNSW tìm kiếm
            search_result = search_engine.search_face(face_encoding)
            
            if not search_result:
                continue
            
            top, right, bottom, left = face_locations[i]
            crop_b64 = crop_face_to_base64(image_rgb, top, right, bottom, left)
            
            face_data = {
                "student_id": search_result['info'].get('MSSV', 'Unknown') if search_result['status'] == 'found' else 'Unknown',
                "name": search_result['info'].get('Ten', 'Unknown') if search_result['status'] == 'found' else 'Unknown',
                "distance": search_result.get('distance', 0),
                "box": [top, right, bottom, left],
                "crop_image": crop_b64
            }
            results.append(face_data)
        
        return jsonify({"faces": results}), 200

    except Exception as e:
        print(f"[ERROR] Loi realtime: {e}")
        return jsonify({"error": str(e)}), 500

# --- CHẠY APP ---
if __name__ == '__main__':
   
    app.run(host='0.0.0.0', port=8000, debug=True)