#!/usr/bin/env python3
"""
Script để xóa các chunks cụ thể khỏi ChromaDB
Sử dụng: python delete_specific_chunks.py
"""

import os
import sys

from dotenv import load_dotenv


# Thêm project root vào path
def get_project_root():
    """Get the root directory of the project."""
    current_dir = os.path.dirname(os.path.abspath(__file__))
    while True:
        if os.path.isdir(os.path.join(current_dir, "data")) and os.path.isdir(
            os.path.join(current_dir, "src")
        ):
            return current_dir
        parent_dir = os.path.dirname(current_dir)
        if parent_dir == current_dir:
            raise FileNotFoundError(
                "Check the project structure. 'data' and 'src' directories not found."
            )
        current_dir = parent_dir


# Setup project paths
root = get_project_root()
sys.path.insert(0, str(root))

load_dotenv()

import chromadb

from configs.logger import get_logger, setup_logging
from src.store_vector.init_index import CHROMA_DB_PATH, COLLECTION_NAME

setup_logging()
logger = get_logger(__name__)

# Danh sách các chunk IDs cần xóa
CHUNKS_TO_DELETE = [
    "61_2020_QH14_CHUONG_VII_Dieu_77_Khoan_12",
    "kê_Dieu_2_Khoan_2",
    "16_2023_QH15_CHUONG_VIII_Dieu_75_Khoan_9",
    "tư_Dieu_2_Khoan_33",
]


def init_local_chroma_index():
    """
    Khởi tạo kết nối ChromaDB local

    Returns:
        tuple: (chroma_client, legal_collection)
    """
    try:
        print(f"Đang kết nối tới ChromaDB local tại: {CHROMA_DB_PATH}")

        # Tạo thư mục nếu chưa tồn tại
        os.makedirs(CHROMA_DB_PATH, exist_ok=True)

        # Khởi tạo client ChromaDB local
        client = chromadb.PersistentClient(path=CHROMA_DB_PATH)

        # Lấy collection
        collection = client.get_collection(name=COLLECTION_NAME)

        logger.info("Kết nối ChromaDB local thành công.")
        logger.info("Collection '%s' đã sẵn sàng.", COLLECTION_NAME)

        return client, collection

    except Exception as e:
        logger.error("Lỗi khi kết nối ChromaDB local: %s", e)
        raise


def delete_chunks_from_chromadb(chunk_ids):
    """
    Xóa các chunk có ID cụ thể khỏi ChromaDB

    Args:
        chunk_ids (list): Danh sách các ID chunk cần xóa

    Returns:
        dict: Kết quả xóa với thông tin thành công/thất bại
    """
    try:
        # Khởi tạo kết nối ChromaDB local
        print("Đang kết nối tới ChromaDB local...")
        chroma_client, legal_collection = init_local_chroma_index()

        # Kiểm tra số lượng documents trước khi xóa
        count_before = legal_collection.count()
        print(f"Số lượng documents trước khi xóa: {count_before}")

        # Kiểm tra xem các chunk_ids có tồn tại trong collection không
        existing_chunks = []
        missing_chunks = []

        print("\nKiểm tra sự tồn tại của các chunks...")
        for chunk_id in chunk_ids:
            try:
                # Kiểm tra chunk có tồn tại không bằng cách query theo ID
                result = legal_collection.get(ids=[chunk_id])
                if result["ids"] and len(result["ids"]) > 0:
                    existing_chunks.append(chunk_id)
                    print(f"✓ Tìm thấy chunk: {chunk_id}")
                else:
                    missing_chunks.append(chunk_id)
                    print(f"✗ Không tìm thấy chunk: {chunk_id}")
            except Exception as e:
                print(f"✗ Lỗi khi kiểm tra chunk {chunk_id}: {e}")
                missing_chunks.append(chunk_id)

        # Xóa các chunks tồn tại
        deleted_chunks = []
        failed_chunks = []

        if existing_chunks:
            print(f"\nĐang xóa {len(existing_chunks)} chunks...")
            try:
                # Xóa các chunks
                legal_collection.delete(ids=existing_chunks)
                deleted_chunks = existing_chunks
                print(f"✓ Đã xóa thành công {len(deleted_chunks)} chunks")

                # Kiểm tra số lượng documents sau khi xóa
                count_after = legal_collection.count()
                print(f"Số lượng documents sau khi xóa: {count_after}")
                print(f"Đã xóa {count_before - count_after} documents")

            except Exception as e:
                print(f"✗ Lỗi khi xóa chunks: {e}")
                failed_chunks = existing_chunks
                deleted_chunks = []
        else:
            print("Không có chunks nào để xóa.")

        return {
            "status": "success" if deleted_chunks else "partial_success",
            "total_requested": len(chunk_ids),
            "deleted_count": len(deleted_chunks),
            "deleted_chunks": deleted_chunks,
            "missing_chunks": missing_chunks,
            "failed_chunks": failed_chunks,
            "documents_before": count_before,
            "documents_after": (
                legal_collection.count() if deleted_chunks else count_before
            ),
        }

    except Exception as e:
        print(f"✗ Lỗi khi xóa chunks khỏi ChromaDB local: {e}")
        return {
            "status": "error",
            "error": str(e),
            "total_requested": len(chunk_ids),
            "deleted_count": 0,
            "deleted_chunks": [],
            "missing_chunks": chunk_ids,
            "failed_chunks": [],
        }


def main():
    """Main function để chạy script xóa chunks"""
    print("=== SCRIPT XÓA CHUNKS KHỎI CHROMADB LOCAL ===")
    print(f"Database path: {CHROMA_DB_PATH}")
    print(f"Collection: {COLLECTION_NAME}")
    print(f"Sẽ xóa {len(CHUNKS_TO_DELETE)} chunks:")
    for i, chunk_id in enumerate(CHUNKS_TO_DELETE, 1):
        print(f"  {i}. {chunk_id}")

    # Xác nhận từ người dùng
    confirmation = input(
        "\nBạn có chắc chắn muốn xóa những chunks này khỏi database LOCAL? (y/N): "
    )
    if confirmation.lower() not in ["y", "yes"]:
        print("Hủy bỏ thao tác xóa.")
        return

    # Thực hiện xóa
    result = delete_chunks_from_chromadb(CHUNKS_TO_DELETE)

    # Hiển thị kết quả
    print("\n=== KẾT QUẢ ===")
    print(f"Trạng thái: {result['status']}")
    print(f"Tổng số chunks yêu cầu xóa: {result['total_requested']}")
    print(f"Số chunks đã xóa thành công: {result['deleted_count']}")

    if result["deleted_chunks"]:
        print("\nChunks đã xóa thành công:")
        for chunk in result["deleted_chunks"]:
            print(f"  ✓ {chunk}")

    if result["missing_chunks"]:
        print("\nChunks không tìm thấy:")
        for chunk in result["missing_chunks"]:
            print(f"  ? {chunk}")

    if result["failed_chunks"]:
        print("\nChunks xóa thất bại:")
        for chunk in result["failed_chunks"]:
            print(f"  ✗ {chunk}")

    if result["status"] == "error":
        print(f"\nLỗi: {result.get('error', 'Unknown error')}")

    print(f"\nTổng số documents trước: {result.get('documents_before', 'N/A')}")
    print(f"Tổng số documents sau: {result.get('documents_after', 'N/A')}")


if __name__ == "__main__":
    main()
