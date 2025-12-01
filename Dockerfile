# 1. Base Image Python 3.8 (Tốt nhất cho dlib/face-recognition)
FROM python:3.8-slim

# 2. Cài đặt thư viện hệ thống (Để build dlib trên Linux)
RUN apt-get update && apt-get install -y \
    build-essential \
    cmake \
    libopenblas-dev \
    liblapack-dev \
    libx11-dev \
    libgtk-3-dev \
    && rm -rf /var/lib/apt/lists/*

# 3. Thiết lập thư mục làm việc chính trong Docker
WORKDIR /app

# 4. Copy requirements (Lưu ý đường dẫn backend/)
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 5. Cài đặt Gunicorn (Nếu chưa có trong requirements.txt thì cài thêm ở đây cho chắc)
RUN pip install gunicorn

# 6. Cài đặt hnswlib (Custom)
COPY backend/hnswlib/ hnswlib/
RUN cd hnswlib && pip install .

# 7. Copy toàn bộ code trong backend vào folder /app/backend trong Docker
COPY backend/ backend/

# 8. Mở port 8000
EXPOSE 8000

# 9. Lệnh chạy server chuẩn Production
# --chdir backend/faces_recognition: Chuyển vào thư mục chứa code trước khi chạy
# server:app : Tìm file server.py và biến app bên trong
CMD ["gunicorn", "--chdir", "backend/faces_recognition", "--bind", "0.0.0.0:8000", "server:app"]