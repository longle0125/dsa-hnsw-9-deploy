import numpy as np
import gradio as gr
import sys
import os
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)
from hnsw import HNSWSearchSystem

SYSTEM = None


def init_system(space='l2', dim=128, max_elements=100000, ef_construction=200, M=16,
                ef_search=100, num_elements=1000, seed=42):
    """
    Khởi tạo index HNSW và sinh dữ liệu.

    Args:
        space: Loại khoảng cách ('l2', 'cosine', 'ip').
        dim: Số chiều vector.
        max_elements: Số phần tử tối đa của index.
        ef_construction: Độ rộng tìm kiếm khi xây dựng.
        M: Số kết nối tối đa mỗi node.
        ef_search: Độ rộng tìm kiếm khi truy vấn.
        num_elements: Số vector ngẫu nhiên để nạp.
        seed: Seed sinh số ngẫu nhiên.
    """
    global SYSTEM
    np.random.seed(int(seed))

    SYSTEM = HNSWSearchSystem(space=space, dim=int(dim))
    SYSTEM.build_hnsw_index(
        max_elements=int(max_elements),
        ef_construction=int(ef_construction),
        M=int(M)
    )
    SYSTEM.set_ef(int(ef_search))
    SYSTEM.generate_data(int(num_elements))

    return f"Khởi tạo thành công.\nspace={space}\ndim={int(dim)}\nnum_elements={int(num_elements)}\nef={int(ef_search)}\nM={int(M)}\ncurrent_count={len(SYSTEM.data)}"


def parse_query_vector(txt: str, dim: int):
    """
    Chuyển chuỗi 'a, b, c, ...' thành mảng (1, dim).

    Args:
        txt: Chuỗi số phẩy theo đúng số chiều.
        dim: Số chiều yêu cầu.
    """
    nums = [x.strip() for x in (txt or "").split(",") if x.strip() != ""]
    arr = np.array([float(v) for v in nums], dtype=np.float32)
    if arr.size != dim:
        raise ValueError(f"Query có {arr.size} phần tử, yêu cầu {dim} phần tử.")
    return arr[None, :]


def search_knn(query_text: str, k: int):
    """
    Tìm K láng giềng gần nhất.

    Args:
        query_text: Vector truy vấn dạng chuỗi số phẩy.
        k: Số lượng kết quả cần trả về.
    """
    if SYSTEM is None or SYSTEM.data is None:
        return "Hệ thống chưa khởi tạo. Hãy bấm 'Khởi tạo & Sinh dữ liệu' trước.", None, None

    try:
        q = parse_query_vector(query_text, SYSTEM.dim)
    except Exception as e:
        return f"Lỗi dữ liệu truy vấn: {e}", None, None

    if int(k) < 1:
        return "Giá trị K phải >= 1.", None, None

    labels, distances = SYSTEM.knn_query(q, k=int(k))
    return "Tìm kiếm hoàn tất.", labels[0].tolist(), distances[0].tolist()


with gr.Blocks(title="HNSW Search (utils)") as demo:
    gr.Markdown("# HNSW Search")
    gr.Markdown(
        "Hướng dẫn: Điều chỉnh thông tin khởi tạo, sau đó nhấn `Khởi tạo và sinh dữ liệu`. Nhập vector truy vấn (đúng `dim`) và chọn K để tìm kiếm."
    )

    # Khởi tạo & sinh dữ liệu
    with gr.Row():
        with gr.Column():
            space = gr.Dropdown(["l2", "cosine", "ip"], value="l2", label="Không gian khoảng cách (space)")
            dim = gr.Number(value=128, precision=0, label="Số chiều (dim)")
            max_elements = gr.Number(value=100000, precision=0, label="Số phần tử tối đa (max_elements)")
        with gr.Column():
            efc = gr.Number(value=200, precision=0, label="ef_construction")
            M = gr.Number(value=16, precision=0, label="M (kết nối tối đa/node)")
            ef_search = gr.Number(value=100, precision=0, label="ef (search)")
        with gr.Column():
            num_elements = gr.Number(value=1000, precision=0, label="Số vector sinh tự động")
            seed = gr.Number(value=42, precision=0, label="Seed")
            init_btn = gr.Button("Khởi tạo và sinh dữ liệu")

    init_out = gr.Textbox(label="Thông tin khởi tạo", lines=6)
    init_btn.click(
        init_system,
        inputs=[space, dim, max_elements, efc, M, ef_search, num_elements, seed],
        outputs=[init_out]
    )

    gr.Markdown("---")

    # Tìm kiếm
    gr.Markdown("## Tìm kiếm K láng giềng gần nhất")
    gr.Markdown("Nhập vector truy vấn dạng số thực, phân tách bởi dấu phẩy, đúng số chiều `dim`.")
    with gr.Row():
        query_text = gr.Textbox(
            label="Vector truy vấn (comma-separated)",
            lines=2
        )
        k_inp = gr.Number(value=5, precision=0, label="K")

    search_btn = gr.Button("Tìm kiếm")
    status = gr.Textbox(label="Trạng thái", lines=1)
    with gr.Row():
        labels_out = gr.JSON(label="Top-K labels")
        dists_out = gr.JSON(label="Top-K distances")

    search_btn.click(
        search_knn,
        inputs=[query_text, k_inp],
        outputs=[status, labels_out, dists_out]
    )

demo.launch(share=True)
