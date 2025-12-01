from pymongo import MongoClient

uri = "mongodb+srv://data_team:ktmt@facereccluster.hjfd7ad.mongodb.net/?retryWrites=true&w=majority&appName=FaceRecCluster"
client = MongoClient(uri)
collection = client['FaceRecProject']['PeopleMetadata']

# Xóa trường feature_vector trong TẤT CẢ các bản ghi
collection.update_many({}, {"$unset": {"feature_vector": ""}})

print("Đã xóa sạch dữ liệu vector cũ. Hãy chạy lại data_import.py!")