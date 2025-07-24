#!/usr/bin/env python3
"""
Script warm up ChromaDB để đảm bảo database sẵn sàng trước khi start API
"""

import logging
import sys
import time
from pathlib import Path


def setup_path():
    """Add project root to Python path"""
    current_dir = Path(__file__).parent.parent
    sys.path.insert(0, str(current_dir))


def setup_logging():
    """Configure logging for the warm up script"""
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )
    return logging.getLogger(__name__)


def warmup_chromadb(logger):
    """
    Warm up ChromaDB by initializing connection and collection

    Args:
        logger: Logger instance for output

    Returns:
        bool: True if successful, False otherwise
    """
    try:
        logger.info("🔥 Starting ChromaDB warm up...")

        # Import sau khi đã setup path
        # pylint: disable=import-outside-toplevel
        from src.store_vector.init_index import init_chroma_index

        # Initialize ChromaDB
        start_time = time.time()
        client, collection = init_chroma_index()

        # Test basic operations
        logger.info("ChromaDB client initialized successfully")

        # Check collection count
        count = collection.count()
        logger.info("Collection contains %d documents", count)

        # Test a simple query if collection has data
        if count > 0:
            try:
                # Test query with a sample
                results = collection.peek(limit=1)
                logger.info("Collection query test successful")
            except Exception as query_error:  # pylint: disable=broad-except
                logger.warning("Collection query test failed: %s", query_error)

        elapsed = time.time() - start_time
        logger.info("ChromaDB warm up completed in %.2f seconds", elapsed)

        return True

    except Exception as error:  # pylint: disable=broad-except
        logger.error("ChromaDB warm up failed: %s", error)
        return False


def warmup_sentence_transformer(logger):
    """
    Warm up sentence transformer model

    Args:
        logger: Logger instance for output

    Returns:
        bool: True if successful, False otherwise
    """
    try:
        logger.info("Starting Sentence Transformer warm up...")

        # pylint: disable=import-outside-toplevel
        from sentence_transformers import SentenceTransformer

        start_time = time.time()
        # Load the model (should be cached from Docker build)
        model = SentenceTransformer("BAAI/bge-m3")

        # Test encoding
        test_text = "This is a test sentence for warm up"
        embedding = model.encode(test_text)

        elapsed = time.time() - start_time
        logger.info("Sentence Transformer warm up completed in %.2f seconds", elapsed)
        logger.info("Test embedding shape: %s", embedding.shape)

        return True

    except Exception as error:  # pylint: disable=broad-except
        logger.error("Sentence Transformer warm up failed: %s", error)
        return False


def main():
    """
    Main warm up function
    """
    # Setup path and logging
    setup_path()
    logger = setup_logging()

    logger.info("Starting AI Legal Assistant warm up sequence...")

    success = True

    # Warm up Sentence Transformer first
    if not warmup_sentence_transformer(logger):
        success = False

    # Small delay
    time.sleep(2)

    # Warm up ChromaDB
    if not warmup_chromadb(logger):
        success = False

    if success:
        logger.info("All warm up tasks completed successfully!")
        sys.exit(0)
    else:
        logger.error("Some warm up tasks failed!")
        sys.exit(1)


if __name__ == "__main__":
    main()
