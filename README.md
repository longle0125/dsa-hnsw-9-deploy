# Face Recognition System with HNSW Search

> Hệ thống nhận diện khuôn mặt và tìm kiếm vector tốc độ cao sử dụng thuật toán HNSW và MongoDB.

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![Flask](https://img.shields.io/badge/Flask-API-green)
![MongoDB](https://img.shields.io/badge/Database-MongoDB-leaf)
![Status](https://img.shields.io/badge/Status-Development-orange)

## Giới thiệu

Dự án này xây dựng một hệ thống định danh thời gian thực (Real-time Identification) với độ trễ thấp. Hệ thống kết hợp giữa **Face Recognition** (trích xuất đặc trưng khuôn mặt) và **HNSW** (Hierarchical Navigable Small World - thuật toán tìm kiếm láng giềng gần nhất) để truy vấn nhanh trên tập dữ liệu lớn.

### Tính năng chính
* **Data Pipeline:** Tự động quét, mã hóa khuôn mặt từ ảnh và đồng bộ metadata + vector lên MongoDB Atlas.
* **Vector Search Engine:** Sử dụng HNSW để tìm kiếm khuôn mặt nhanh hơn và hiệu quả hơn phương pháp Brute-force truyền thống.
* **API Service:** Backend Flask cung cấp API cho cả upload file và webcam streaming (Base64).
* **Visualization:** Công cụ mô phỏng trực quan cách thuật toán HNSW hoạt động trên không gian 2D/3D.

---
## Hướng dẫn Cài đặt & Triển khai

*Lưu ý: chỉ tương thích tốt nhất với Python 3.8. Vui lòng không sử dụng phiên bản khác để tránh lỗi thư viện face-recognition đã build sẵn.*

### Cài đặt môi trường
```
# 1. Clone repository về máy
git clone https://github.com/Dat-2536/dsa-hnsw-9.git


# 2. Tạo môi trường ảo với Python 3.8
# (Đảm bảo bạn đã cài Python 3.8 trên máy) 
py -3.8 -m venv env

# 3. Kích hoạt môi trường
# - Trên Windows:
env\Scripts\activate
# - Trên Linux/Mac:
source env/bin/activate
```

### Sử dụng các thư viện cần thiết
```
# Cài đặt các thư viện chung (Flask, Numpy, PyMongo, v.v.)
cd backend
pip install -r requirements.txt
```
### Sử dụng thư viện hnswlib đã được chỉnh sửa
```
# Di chuyển vào thư mục source code của thư viện
cd hnswlib
# Cài đặt thư viện vào môi trường hiện tại
pip install 
cd ..
cd ..
```
### Để sử dụng thư viện face-recognition cho windows
xem chi tiết ở https://www.geeksforgeeks.org/installation-guide/how-to-install-face-recognition-in-python-on-windows/

## sử dụng
### 1. Để nạp dữ liệu vào database
```python data_import.py```
### 2. Khởi động server
Bật API Backend để bắt đầu nhận diện.
```python server.py ```

- Server sẽ chạy tại: https://face-reco-api-2sjf.onrender.com

- Sẵn sàng nhận request.

### 3. khởi động frontend
- di chuyển đến thư mục frontend
- npm run dev
- truy cập vào địa chỉ ip
## Chạy các demo
### So sánh tốc độ (Benchmark):
```python demos/benchmark.py```
### Mô phỏng thuật toán (Visualize):
```python demos/visualize.py```

## API Documentation
### 1. Nhận diện qua Webcam (Realtime)
- URL: ```/recognize_frame```
- Method: ```POST```
- Content-Type: ```application/json```
- Body:
``` 
{
 "image": "data:image/jpeg;base64,/9j/4AAQSkZJRgABAQAAAQABAAD..."
}
```
- Response (Success):
```
{
    "faces": [
        {
            "student_id": "2011001",
            "name": "Nguyen Van A",
            "distance": 0.35,
            "box": [100, 200, 300, 400],
            "crop_image": ""
        }
    ]
}
```
### 2. Nhận diện qua File ảnh
- URL: ```/recognize_image``
- Method: ```POST```
- Body: ```form-data (key=file)```

## Google Colab
- [Mô phỏng quá trình tìm kiếm sử dụng đồ thị HNSW](https://colab.research.google.com/drive/12AIafk-Fpl572KC7bbj-SmKZucqr3K7W?usp=sharing)

- [So sánh giữa HNSW và Brute Force](https://colab.research.google.com/drive/1QEikK7hTZ6dJoA7pDZ_SpIHq9lGO_HW1#scrollTo=l2xGFl2BFzEk)
- [Mô phỏng kết quả của việc truy vấn một vector ngẫu nhiên](https://colab.research.google.com/drive/1dWbGTWvKGRy7o77not6ntFy-LrmREYCj#scrollTo=BZ57eTlREtOW)
## 👥 Thành viên thực hiện
| Tên | MSSV | Vai trò |
|----------|----------|----------|
| Lê Hoàng Long| 2411915 | Backend |
| Nguyễn Tiến Đạt| 2410712 | Frontend |
| Nguyễn Hoàng Minh | 2412084 | Data |