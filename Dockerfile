# Sử dụng Python 3.8 Slim
FROM python:3.8-slim

# 1. Cài đặt công cụ biên dịch (Bắt buộc cho dlib và hnswlib)
RUN apt-get update && apt-get install -y \
    build-essential \
    cmake \
    libopenblas-dev \
    liblapack-dev \
    libx11-dev \
    libgtk-3-dev \
    libgl1 \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# 2. Cài đặt các thư viện đại chúng trước (để tận dụng cache)
COPY backend/requirements.txt .
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# 3. Copy toàn bộ code vào (bao gồm cả thư mục backend/hnswlib)
COPY . .

# -----------------------------------------------------------
# 4. BƯỚC QUAN TRỌNG: Cài đặt thư viện HNSW 
# -----------------------------------------------------------
RUN pip install ./backend/hnswlib

# 5. Thiết lập thư mục làm việc để chạy server
WORKDIR /app/backend/faces_recognition

# 6. Mở port và chạy
EXPOSE 8000
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--timeout", "120", "server:app"]