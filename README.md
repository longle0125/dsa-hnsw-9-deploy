# Face Recognition System with HNSW

> Hệ thống nhận diện khuôn mặt và tìm kiếm vector tốc độ cao sử dụng thuật toán HNSW và MongoDB Atlas.

## 🌐 Demo Trực tuyến

  * **Landing Page:** [https://dat-2536.github.io/dsa-hnsw-9/](https://dat-2536.github.io/dsa-hnsw-9/)
  * **Web App (Live):** [https://dsa-hnsw-9.vercel.app](https://dsa-hnsw-9.vercel.app)

## 📖 Giới thiệu

Dự án này xây dựng một hệ thống định danh thời gian thực (Real-time Identification) với độ trễ thấp, được thiết kế tối ưu cho môi trường Cloud. Hệ thống kết hợp giữa **Face Recognition** (trích xuất đặc trưng khuôn mặt) và **HNSW** (Hierarchical Navigable Small World) để truy vấn nhanh trên tập dữ liệu lớn.

### Kiến trúc hệ thống

1.  **Backend (Flask):** Xử lý API, nhận diện khuôn mặt và tìm kiếm vector (HNSW). Deploy trên Render.
2.  **Frontend (React + Vite):** Giao diện người dùng hiện đại, xử lý webcam đa luồng để hiển thị mượt mà.
3.  **Database (MongoDB Atlas):** Lưu trữ metadata và feature vectors trên Cloud.

-----

## 🛠 Hướng dẫn Cài đặt Local (Dành cho Developer)

### Yêu cầu tiên quyết

  * **Python:** 3.8 hoặc 3.9 (Khuyên dùng 3.8 để tương thích tốt nhất).
  * **Node.js:** Phiên bản 16 trở lên.
  * **C++ Build Tools:** Cần cài đặt CMake và Visual Studio C++ Build Tools (trên Windows) để biên dịch `dlib`.

### 1\. Cài đặt Backend

```bash
# 1. Di chuyển vào thư mục backend
cd backend

# 2. Tạo môi trường ảo
python -m venv .venv

# 3. Kích hoạt môi trường
# - Windows:
.venv\Scripts\activate
# - Linux/Mac:
source .venv/bin/activate

# 4. Cài đặt thư viện
pip install -r requirements.txt

# 5. Cài đặt thư viện hnswlib tùy chỉnh
cd hnswlib
pip install .
cd ..
```

**Cấu hình biến môi trường Backend:**
Tạo file `.env` trong thư mục `backend/` với nội dung:

```properties
# Connection String lấy từ MongoDB Atlas
MONGO_URI=mongodb+srv://<user>:<password>@cluster0.xxxxx.mongodb.net/?retryWrites=true&w=majority
```

### 2\. Cài đặt Frontend

```bash
# 1. Mở terminal mới, di chuyển vào thư mục frontend
cd frontend

# 2. Cài đặt dependencies
npm install
```

**Cấu hình biến môi trường Frontend:**
Tạo file `.env` trong thư mục `frontend/` (ngang hàng `package.json`):

```properties
# Trỏ về Backend (Local hoặc Render)
VITE_BACKEND_URL=http://localhost:8000
```

-----

## 🚀 Hướng dẫn Sử dụng

### 1\. Nạp dữ liệu (Data Import)

Quét ảnh trong thư mục `Demo_Final_Images`, tạo vector và đẩy lên MongoDB Atlas.

```bash
# Tại thư mục backend (đã activate venv)
python faces_recognition/data_import.py
```

### 2\. Khởi động Backend

```bash
# Tại thư mục backend
python app.py
```

  * Server sẽ chạy tại: `http://localhost:8000`

### 3\. Khởi động Frontend

```bash
# Tại thư mục frontend
npm run dev
```

  * Truy cập Web App tại: `http://localhost:5173`

-----

## 🧪 Chạy các Demo

Các script này dùng để kiểm thử hiệu năng thuật toán mà không cần chạy toàn bộ server web.

### So sánh tốc độ (Benchmark):

So sánh thời gian truy vấn giữa HNSW và Linear Search (Brute-force).

```bash
python demos/benchmark.py
```

### Mô phỏng thuật toán (Visualize):

Trực quan hóa cách HNSW tìm đường đi trong không gian vector.

```bash
python demos/visualize.py
```

-----

## 📡 API Documentation

### 1\. Nhận diện qua Webcam (Realtime)

  * **URL:** `/recognize_frame`
  * **Method:** `POST`
  * **Content-Type:** `application/json`
  * **Body:**
    ```json
    {
      "image": "data:image/jpeg;base64,/9j/4AAQSkZJRgABAQ..."
    }
    ```
  * **Response (Success):**
    ```json
    {
        "faces": [
            {
                "student_id": "2011001",
                "name": "Nguyen Van A",
                "distance": 0.35,
                "box": [100, 200, 300, 400],
                "crop_image": "data:image/jpeg;base64..."
            }
        ]
    }
    ```

### 2\. Nhận diện qua File ảnh

  * **URL:** `/recognize_image`
  * **Method:** `POST`
  * **Body:** `multipart/form-data` (key=`file`)

-----

## 📊 Google Colab Resources

  * [Mô phỏng quá trình tìm kiếm sử dụng đồ thị HNSW](https://colab.research.google.com/drive/12AIafk-Fpl572KC7bbj-SmKZucqr3K7W?usp=sharing)
  * [So sánh giữa HNSW và Brute Force](https://colab.research.google.com/drive/1QEikK7hTZ6dJoA7pDZ_SpIHq9lGO_HW1#scrollTo=l2xGFl2BFzEk)
  * [Mô phỏng kết quả của việc truy vấn một vector ngẫu nhiên](https://colab.research.google.com/drive/1dWbGTWvKGRy7o77not6ntFy-LrmREYCj#scrollTo=BZ57eTlREtOW)

## 👥 Thành viên thực hiện (HCMUT - Honors Program)

| Tên | MSSV | Vai trò |
|----------|----------|----------|
| **Lê Hoàng Long** | 2411915 | Backend & Algorithm |
| **Nguyễn Tiến Đạt** | 2410712 | Frontend & Deployment |
| **Nguyễn Hoàng Minh** | 2412084 | Data Pipeline & Database |