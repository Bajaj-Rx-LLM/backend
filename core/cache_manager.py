import chromadb
from chromadb.utils import embedding_functions

class CacheManager:
    """
    Manages the ChromaDB cache to store and retrieve document vectors.
    """
    def __init__(self, host: str = "localhost", port: int = 8000):
        try:
            self.client = chromadb.HttpClient(host=host, port=port)
            self.embedding_function = embedding_functions.SentenceTransformerEmbeddingFunction(
                model_name="all-MiniLM-L6-v2"
            )
            self.collection = self.client.get_or_create_collection(
                name="hackrx_document_cache",
                embedding_function=self.embedding_function
            )
            print("✅ ChromaDB cache connected successfully.")
        except Exception as e:
            print(f"❌ Failed to connect to ChromaDB: {e}")
            self.client = None

    def check_if_processed(self, doc_id: str) -> bool:
        """
        Checks if a document with the given ID has already been processed and cached.
        """
        results = self.collection.get(where={"doc_id": doc_id}, limit=1)
        return len(results['ids']) > 0

    def add_to_cache(self, doc_id: str, chunks: list[str]):
        """
        Adds document chunks to the cache. Each chunk is tagged with the doc_id.
        """
        chunk_ids = [f"{doc_id}_{i}" for i in range(len(chunks))]
        metadatas = [{"doc_id": doc_id} for _ in chunks]
        
        self.collection.add(
            documents=chunks,
            metadatas=metadatas,
            ids=chunk_ids
        )
        print(f"✅ Document '{doc_id}' added to cache with {len(chunks)} chunks.")

    def query_cache(self, doc_id: str, query_text: str, n_results: int = 3) -> list[str]:
        """
        Queries the cache for relevant chunks for a specific document.
        """
        results = self.collection.query(
            query_texts=[query_text],
            where={"doc_id": doc_id}, # CRITICAL: Filter to only search within the correct document
            n_results=n_results
        )
        return results['documents'][0] if results['documents'] else []
