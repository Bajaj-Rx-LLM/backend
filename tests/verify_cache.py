# Note: This script needs to be able to import from your 'core' and 'utils' directories.
# To run it from the root 'hackrx-backend/' folder, use: python -m tests.verify_cache
import sys
import os

# Add the project root to the Python path to allow for absolute imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from core.cache_manager import CacheManager
from utils.helpers import create_document_id

# The same URL you used in the test request
TEST_PDF_URL = "https://bitcoin.org/bitcoin.pdf"

def check_cache_for_document(url: str):
    """
    Connects to ChromaDB and verifies if a document has been ingested.
    """
    print("--- Connecting to ChromaDB to verify cache ---")
    cache = CacheManager()
    
    if not cache.client:
        print("Could not connect to ChromaDB. Aborting.")
        return

    # Generate the same ID that the main app would have created
    doc_id = create_document_id(url)
    print(f"Checking for document with ID: {doc_id}")

    # Use the manager to check if the document exists
    is_processed = cache.check_if_processed(doc_id)

    if is_processed:
        print(f"\n✅ SUCCESS: Document '{doc_id}' found in the cache.")
        
        # As a bonus, let's retrieve a few chunks to be sure
        results = cache.collection.get(
            where={"doc_id": doc_id},
            limit=3,
            include=["documents", "metadatas"]
        )
        print("\n--- Sample Chunks Retrieved ---")
        for i, doc in enumerate(results['documents']):
            print(f"Chunk {i+1}: {doc[:100]}...") # Print the first 100 chars
            print(f"  Metadata: {results['metadatas'][i]}\n")
            
    else:
        print(f"\n❌ FAILED: Document '{doc_id}' was NOT found in the cache.")


if __name__ == "__main__":
    check_cache_for_document(TEST_PDF_URL)
