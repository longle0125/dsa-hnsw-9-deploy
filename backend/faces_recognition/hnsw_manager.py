import numpy as np
from pymongo import MongoClient
import sys
import os


current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)


try:
    from hnsw import HNSWSearchSystem
except ImportError:
        print("[WARN] Không tìm thấy module 'hnsw'")

from dotenv import load_dotenv
load_dotenv()

class FaceSearchEngine:
    def __init__(self):
        # Cấu hình MongoDB
        self.uri = os.getenv("MONGO_URI")
        if not self.uri:
             raise ValueError("Chưa cấu hình MONGO_URI trong file .env")
        self.client = MongoClient(self.uri)
        self.collection = self.client['FaceRecProject']['PeopleMetadata']
        
        # Khởi tạo search system
        self.dim = 128
        self.search_system = None
        
        # Nếu import được class wrapper thì dùng, không thì dùng thư viện gốc
        if HNSWSearchSystem:
            self.search_system = HNSWSearchSystem(space='l2', dim=self.dim)
        else:
            # Fallback dùng trực tiếp thư viện gốc nếu không có wrapper
            import hnswlib
            self.search_system = hnswlib.Index(space='l2', dim=self.dim)

        self.metadata_mapping = {}
    
    def load_data_and_build_index(self):
        print("Đang tải dữ liệu vector từ MongoDB...")
        cursor = self.collection.find({"feature_vector": {"$exists": True}})
        
        vectors = []
        ids = []
        self.metadata_mapping = {}
        current_id = 0
        
        for doc in cursor:
            vec = doc['feature_vector']
            
            if isinstance(vec, list) and len(vec) == 128:
                vectors.append(vec)
                ids.append(current_id)
                
                self.metadata_mapping[current_id] = {
                    "MSSV": doc.get("MSSV", "Unknown"),
                    "Ten": doc.get("Ten", "Unknown"),
                    "MongoID": str(doc["_id"])
                }
                current_id += 1
            
        if len(vectors) == 0:
            print("Database rỗng hoặc chưa chạy data_import.py!")
            return

        print(f"Đã tải {len(vectors)} vector. Đang xây dựng HNSW Index...")

        # Xây dựng index bằng phương thức của class HNSWSearchSystem
        # Lưu ý: Class wrapper của bạn có method build_hnsw_index và add_items
        if hasattr(self.search_system, 'build_hnsw_index'):
             self.search_system.build_hnsw_index(
                max_elements=len(vectors) + 1000, 
                ef_construction=200, 
                M=16
            )
             self.search_system.add_items(np.array(vectors), np.array(ids))
             self.search_system.set_ef(50)
        else:
            # Fallback cho thư viện gốc hnswlib (nếu không dùng wrapper)
            self.search_system.init_index(max_elements=len(vectors) + 1000, ef_construction=200, M=16)
            self.search_system.add_items(np.array(vectors), np.array(ids))
            self.search_system.set_ef(50)
        
        # Lấy kích thước index (wrapper có hàm get_size, thư viện gốc có get_current_count)
        size = self.search_system.get_size() if hasattr(self.search_system, 'get_size') else self.search_system.get_current_count()
        print(f"Xây dựng xong Index với {size} phần tử!")
    
    def search_face(self, query_vector):
        """
        Input: query_vector (list hoặc numpy array 128 chiều)
        """
        # Kiểm tra xem index đã build chưa
        is_built = False
        if hasattr(self.search_system, 'is_built'):
            is_built = self.search_system.is_built
        else:
            # Thư viện gốc coi như đã build nếu đã init
            is_built = True 

        if self.search_system is None or not is_built:
            print("Lỗi: Chưa build index.")
            return None

        # Query
        query_np = np.array([query_vector])
        
        try:
            # Dùng hàm knn_query của wrapper hoặc thư viện gốc
            labels, distances = self.search_system.knn_query(query_np, k=1)
            
            found_id = labels[0][0]
            distance = distances[0][0]
            
            # Ngưỡng (Threshold): 0.5 - 0.6 là mức trung bình cho Euclidean Distance (l2)
            if distance > 0.5: 
                return {"status": "unknown", "distance": float(distance)}
                
            info = self.metadata_mapping.get(found_id)
            return {
                "status": "found",
                "info": info,
                "distance": float(distance)
            }
        except Exception as e:
            print(f"Lỗi khi search vector: {e}")
            return None

# --- PHẦN TEST ---
if __name__ == "__main__":
    engine = FaceSearchEngine()
    engine.load_data_and_build_index()
    
    # Test thử với vector ngẫu nhiên
    dummy_vec = np.random.rand(128)
    print("Test Search Result:", engine.search_face(dummy_vec))