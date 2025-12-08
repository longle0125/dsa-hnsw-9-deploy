# Sử dụng Image đã cài sẵn dlib và face_recognition (Tiết kiệm 20 phút build)
FROM animation/face_recognition:latest

# Vì image này dùng Python 3, ta thiết lập thư mục làm việc
WORKDIR /app

# Copy file requirements (Lưu ý bỏ dòng dlib và face-recognition trong file này đi nếu muốn chắc chắn, 
# nhưng pip thông minh sẽ tự nhận diện là đã cài rồi)
COPY backend/requirements.txt .

# Cài các thư viện còn lại (Flask, Numpy, Mongo...)
# Image này đã có sẵn numpy, dlib, face_recognition rồi.
RUN pip install --no-cache-dir -r requirements.txt

# Cài hnswlib
COPY backend/hnswlib/ hnswlib/
RUN cd hnswlib && pip install .

# Copy code
COPY backend/ backend/

EXPOSE 8000

# Image này dùng python3, ta gọi waitress
CMD ["waitress", "--chdir", "backend", "--bind", "0.0.0.0:8000", "app:app"]