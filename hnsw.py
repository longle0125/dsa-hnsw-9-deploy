import hnswlib
import numpy as np
import pickle

class HNSWSearchSystem:
    def __init__(self, space: str = 'l2', dim: int = 16):
        """
        Khởi tạo hệ thống tìm kiếm

        Args:
            space: Không gian khoảng cách ('l2', 'cosine', 'ip')
            dim: Số chiều của vector
        """
        self.space = space
        self.dim = dim
        self.index = hnswlib.Index(space, dim)
        self.data = None
        self.labels = None
        self.is_built = False

    def build_hnsw_index(self, max_elements: int = 10000, ef_construction: int = 200, M: int = 128) -> None:
            """
            Xây dựng chỉ mục HNSW

            Args:
                data: Dữ liệu vector
                max_elements: Số lượng phần tử tối đa
                ef_construction: Tham số ef cho quá trình xây dựng
                M: Tham số M (số lượng kết nối tối đa)
            """
            #xây dựng index
            self.max_elements = max_elements
            self.ef_construction = ef_construction
            self.M = M
            self.is_built = True
            self.index.init_index(max_elements, ef_construction, M)

    def set_ef(self, val: int):
         # higher ef leads to better accuracy, but slower search
         self.ef_search = val
         self.index.set_ef(val)

    def set_num_threads(self, val: int):
         # Set number of threads used during batch search/construction
         # By default using all available cores
         self.num_threads = val
         self.index.set_num_threads(val)

    def add_items(self, data: np.ndarray,  ids: np.ndarray = None) -> None:
        """
        Thêm các phần tử vào index

        Args:
            data: Dữ liệu vector cần thêm
            ids: ID của các vector (nếu None sẽ tự động tạo theo thứ tự tăng dần)
        """
        if not self.is_built:
            raise ValueError("Chưa build index! Gọi build_hnsw_index() trước.")

        self.data = data
        if ids is None:
            # Added elements will have consecutive ids
            ids = np.arange(len(data))
        self.labels = ids

        self.index.add_items(data, ids)

    def generate_data(self, num_elements:int) -> None:
         #Tạo ngẫu nhiên một só các vector để add vào đồ thị
         data = np.float32(np.random.random((num_elements, self.dim)))
         self.add_items(data)

    def knn_query(self, query: np.ndarray, k: int = 1) -> tuple:
        """
        Tìm kiếm K láng giềng gần nhất

        Args:
            query: Vector truy vấn (có thể là 1 vector hoặc nhiều vector)
            k: Số lượng kết quả trả về

        Returns:
            (labels, distances): Tuple chứa nhãn và khoảng cách của K kết quả gần nhất
        """
        if not self.is_built:
            raise ValueError("Chưa build index! Gọi build_hnsw_index() trước.")

        labels, distances = self.index.knn_query(query, k)
        return labels, distances

    def create_copy(self) -> 'HNSWSearchSystem':
        """
        Tạo bản Deep copy của hệ thống (dùng pickle round-trip)
        """
        # Tạo bản copy của index HNSW
        index_copy = pickle.loads(pickle.dumps(self.index))

        # Tạo hệ thống mới
        new_system = HNSWSearchSystem(self.space, self.dim)
        new_system.index = index_copy
        new_system.data = self.data.copy() if self.data is not None else None
        new_system.labels = self.labels.copy() if self.labels is not None else None
        new_system.is_built = self.is_built
        new_system.max_elements = self.max_elements
        new_system.ef_construction = self.ef_construction
        new_system.M = self.M
        new_system.ef_search = self.ef_search

        return new_system