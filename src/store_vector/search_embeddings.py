import os
import sys
import time

from dotenv import load_dotenv
from sentence_transformers import SentenceTransformer

load_dotenv()


def get_project_root():
    """Get the root directory of the project."""
    current_dir = os.path.dirname(os.path.abspath(__file__))
    while True:
        # Kiểm tra xem 'data' và 'src' có tồn tại trong thư mục hiện tại không
        if os.path.isdir(os.path.join(current_dir, "data")) and os.path.isdir(
            os.path.join(current_dir, "src")
        ):
            return current_dir

        parent_dir = os.path.dirname(current_dir)
        if parent_dir == current_dir:  # Đã đến thư mục gốc của hệ thống
            raise FileNotFoundError(
                "Check the project structure. 'data' and 'src' directories not found."
            )
        current_dir = parent_dir


# Set up logging
root = get_project_root()
sys.path.insert(0, str(root))

from configs.logger import get_logger, setup_logging
from src.store_vector.init_index import init_chroma_index

setup_logging()
logger = get_logger(__name__)
collection = init_chroma_index()[1]

# Cấu hình model có thể thay đổi
DEFAULT_MODEL = "BAAI/bge-m3"
# DEFAULT_MODEL = "all-MiniLM-L6-v2"
ALTERNATIVE_MODELS = {
    "vietnamese": "keepitreal/vietnamese-sbert",
    "multilingual": "paraphrase-multilingual-MiniLM-L12-v2",
    "fast": "all-MiniLM-L6-v2",
    "quality": "all-mpnet-base-v2",
    "lightweight": "distiluse-base-multilingual-cased",
}


def get_sentence_transformer(model_name=None):
    """Get SentenceTransformer model instance."""
    if model_name is None:
        model_name = DEFAULT_MODEL
    elif model_name in ALTERNATIVE_MODELS:
        model_name = ALTERNATIVE_MODELS[model_name]

    logger.info("Loading SentenceTransformer model: %s", model_name)
    return SentenceTransformer(model_name)


def search_relevant_embeddings(text, n_results=5, model_name=None):
    start_time = time.time()

    # Sử dụng function helper để get model
    model = get_sentence_transformer(model_name)
    embedding_from_text = model.encode(text, normalize_embeddings=True)
    start_query_time = time.time()
    results = collection.query(
        query_embeddings=embedding_from_text,
        n_results=n_results,
        # where={"source": "article"},        # Tùy chọn: Lọc theo metadata (AND logic)
        # where_document={"$contains":"leave"} # Tùy chọn: Lọc theo nội dung document
    )
    end_query_time = time.time()

    # Tính cosine similarity từ distances (ChromaDB trả về cosine distances)
    # Cosine similarity = 1 - cosine distance
    logger.info(
        "Time to run with retrieving is %f",
        float(end_query_time - start_query_time),
    )
    cosine_similarities = []
    if results["distances"] and len(results["distances"][0]) > 0:
        cosine_similarities = [1 - distance for distance in results["distances"][0]]
    # Tạo dictionary mới với cosine similarities
    enhanced_results = {
        "ids": results["ids"],
        "distances": results["distances"],
        "metadatas": results["metadatas"],
        "documents": results["documents"],
        "embeddings": results["embeddings"],
        "cosine_similarities": [cosine_similarities],
    }
    end_time = time.time()
    logger.info("Time to run search_embeddings is %f", float(end_time - start_time))
    return enhanced_results


if __name__ == "__main__":
    test_text = "Chương I điều 2 bộ luật hình sự."

    # Test với model mặc định
    print("=== Testing with default model ===")
    res = search_relevant_embeddings(test_text, 5)

    # Test với model tiếng Việt (nếu có)
    print("\n=== Testing with Vietnamese model ===")
    try:
        res_vn = search_relevant_embeddings(test_text, 5, model_name="vietnamese")
        print("Vietnamese model loaded successfully")
    except (ImportError, OSError, ValueError) as e:
        print("Vietnamese model failed: %s", e)
        res_vn = res

    if res["documents"] and len(res["documents"][0]) > 0:
        print("Documents:")
        for i, doc in enumerate(res["documents"][0]):
            print(f"  {i+1}. {doc[:100]}...")

        print("\nCosine Similarities:")
        for i, score in enumerate(res["cosine_similarities"][0]):
            print(f"  {i+1}. {score:.4f}")
    else:
        print("No documents found.")
