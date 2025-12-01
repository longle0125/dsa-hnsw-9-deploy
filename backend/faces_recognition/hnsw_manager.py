import numpy as np
from pymongo import MongoClient
import sys
import os
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)
from backend.hnsw import HNSWSearchSystem

class FaceSearchEngine:
    def __init__(self):
        self.uri = "mongodb+srv://data_team:ktmt@facereccluster.hjfd7ad.mongodb.net/?retryWrites=true&w=majority&appName=FaceRecCluster"
        self.client = MongoClient(self.uri)
        self.collection = self.client['FaceRecProject']['PeopleMetadata']
        
        self.search_system = None
        self.metadata_mapping = {}
    
    def load_data_and_build_index(self):
        print("Đang tải dữ liệu vector từ MongoDB...")
        # Lấy những người ĐÃ CÓ feature_vector
        cursor = self.collection.find({"feature_vector": {"$exists": True}})
        
        vectors = []
        ids = []
        self.metadata_mapping = {}
        current_id = 0
        for doc in cursor:
            vec = doc['feature_vector']
            print(vec)
            # Đảm bảo vector đúng kích thước 128 chiều
            if isinstance(vec, list) and len(vec) == 128:
                vectors.append(vec)
                ids.append(current_id)
                
                # Mapping: ID số (HNSW) --> Thông tin thật (Mongo)
                self.metadata_mapping[current_id] = {
                    "MSSV": doc.get("MSSV", "Unknown"),
                    "Ten": doc.get("Ten", "Unknown"),
                    "MongoID": str(doc["_id"])
                }
                current_id += 1
            else:
                print(f"Dữ liệu lỗi (ID: {doc.get('_id')} - {doc.get('Ten')}): vector không hợp lệ.")
            
            if len(vectors) == 0:
                print("Database rỗng hoặc chưa chạy update_vectors()!")
                return
            
            print(f"Đã tải {len(vectors)} vector. Đang khởi tạo HNSWSearchSystem...")

        dim = 128
        self.search_system = HNSWSearchSystem(space='l2', dim=dim) #
        

        self.search_system.build_hnsw_index(
            max_elements=len(vectors) + 1000, 
            ef_construction=200, 
            M=16
        ) 
        
        # Thêm dữ liệu vào index
        self.search_system.add_items(np.array(vectors), ids) #
        
        # Cấu hình độ chính xác tìm kiếm (ef_search)
        self.search_system.set_ef(50) #
        
        print(f"Xây dựng xong Index với {self.search_system.get_size()} phần tử!")
    
    def search_face(self, query_vector):
        """
        Input: query_vector (list hoặc numpy array 128 chiều)
        """
        if self.search_system is None or not self.search_system.is_built:
            print("Lỗi: Chưa build index.")
            return None

        # Chuyển vector về dạng numpy array 2D (1, 128) để query
        query_np = np.array([query_vector])
        
        # Gọi hàm knn_query từ file hnsw.py
        # k=1: Tìm người giống nhất
        labels, distances = self.search_system.knn_query(query_np, k=1) #
        
        found_id = labels[0][0]
        distance = distances[0][0]
        
        # Ngưỡng chấp nhận (Threshold)
        if distance > 0.5: 
            return {"status": "unknown", "distance": float(distance)}
            
        info = self.metadata_mapping.get(found_id)
        return {
            "status": "found",
            "info": info,
            "distance": float(distance)
        }

# --- PHẦN TEST ---
if __name__ == "__main__":
    engine = FaceSearchEngine()
    engine.load_data_and_build_index()
    
    # Test thử với vector ngẫu nhiên
    dummy_vec = np.random.rand(128)
    print("Test Search Result:", engine.search_face(dummy_vec))