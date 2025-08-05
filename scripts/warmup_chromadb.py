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
    Warm up API embedding connection

    Args:
        logger: Logger instance for output

    Returns:
        bool: True if successful, False otherwise
    """
    try:
        logger.info("Starting API embedding warm up...")

        # pylint: disable=import-outside-toplevel
        from gradio_client import Client

        start_time = time.time()
        # Test API connection
        client = Client("hieuailearning/BAAI_bge_m3_api")

        # Test encoding with API
        test_text = "This is a test sentence for warm up"
        embedding = client.predict(text_input=test_text, api_name="/predict")

        elapsed = time.time() - start_time
        logger.info("API embedding warm up completed in %.2f seconds", elapsed)
        logger.info("Test embedding length: %d", len(embedding) if embedding else 0)

        return True

    except Exception as error:  # pylint: disable=broad-except
        logger.error("API embedding warm up failed: %s", error)
        return False


def main():
    """
    Main warm up function
    """
    # Setup path and logging
    setup_path()
    logger = setup_logging()

    # Check if this is post-startup warm up
    is_post_startup = len(sys.argv) > 1 and sys.argv[1] == "--post-startup"

    if is_post_startup:
        logger.info("Starting AI Legal Assistant POST-STARTUP warm up sequence...")
    else:
        logger.info("Starting AI Legal Assistant PRE-STARTUP warm up sequence...")

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
        if is_post_startup:
            logger.info("Post-startup warm up completed successfully!")
        else:
            logger.info("Pre-startup warm up completed successfully!")
        sys.exit(0)
    else:
        logger.error("Some warm up tasks failed!")
        sys.exit(1)


if __name__ == "__main__":
    main()
