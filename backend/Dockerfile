# 1. Dùng Python 3.9 Slim để nhẹ nhất có thể
FROM python:3.9-slim

# 2. Cài đặt các công cụ hệ thống cần thiết cho dlib và opencv
# (Render không có sẵn mấy cái này nên phải cài thủ công)
RUN apt-get update && apt-get install -y \
    build-essential \
    cmake \
    libopenblas-dev \
    liblapack-dev \
    libx11-dev \
    libgtk-3-dev \
    libgl1 \
    && rm -rf /var/lib/apt/lists/*

# 3. Thiết lập thư mục làm việc trong container
WORKDIR /app

# 4. Copy requirements.txt trước để tận dụng cache
COPY requirements.txt .

# 5. Cài đặt thư viện (Quá trình này sẽ mất khoảng 5-10 phút khi build lần đầu vì dlib)
RUN pip install --no-cache-dir -r requirements.txt
# Cài thêm Gunicorn nếu chưa có trong requirements
RUN pip install gunicorn

# 6. Copy toàn bộ code lên
COPY . .

# 7. Mở port 10000 (Render thường thích port này hoặc bạn cấu hình sau)
EXPOSE 8000

# 8. Lệnh chạy server (Quan trọng)
# app:app nghĩa là: file app.py, tìm biến tên là app (biến Flask)
CMD ["gunicorn", "-w", "2", "-b", "0.0.0.0:8000", "app:app"]