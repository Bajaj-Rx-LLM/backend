from .cache_manager import CacheManager
from .document_processor import DocumentProcessor
from utils.helpers import create_document_id
from api.models import HackRxRequest # We will define this model next

# --- Placeholder for the actual LLM call ---
def get_llm_answer(question: str, context: list[str]) -> str:
    """
    This is a placeholder function.
    In a real application, this function would:
    1. Construct a detailed prompt with the question and context.
    2. Make an API call to an LLM (like GPT-4 or Gemini).
    3. Return the LLM's generated answer.
    """
    print(f"\n--- Calling LLM for question: '{question}' ---")
    print(f"Context found: {len(context)} chunks")
    
    # For the hackathon, you MUST replace this with a real LLM call.
    # For now, it returns a dummy answer.
    if not context:
        return "I could not find relevant information in the document to answer this question."
        
    return f"This is a placeholder answer for the question '{question}' based on the provided context."
# --- End of placeholder ---


class RAGService:
    """
    The main service that orchestrates the entire RAG pipeline for a request.
    """
    def __init__(self):
        self.cache = CacheManager()
        self.processor = DocumentProcessor()

    def process_request(self, request: HackRxRequest) -> list[str]:
        doc_url = request.documents
        questions = request.questions
        
        doc_id = create_document_id(doc_url)
        print(f"Processing request for document ID: {doc_id}")

        # 1. Check if the document is already in our cache
        if not self.cache.check_if_processed(doc_id):
            print(f"Cache miss for document ID: {doc_id}. Starting ingestion...")
            # If not, process and add it to the cache
            chunks = self.processor.process_pdf_from_url(doc_url)
            if chunks:
                self.cache.add_to_cache(doc_id, chunks)
            else:
                # Handle case where document processing fails
                return ["Failed to process the document from the provided URL." for _ in questions]
        else:
            print(f"Cache hit for document ID: {doc_id}. Skipping ingestion.")

        # 2. Loop through each question and generate an answer
        final_answers = []
        for q in questions:
            # a. Find relevant context from the cache
            context_chunks = self.cache.query_cache(doc_id, q)
            
            # b. Call the LLM with the question and context to get the final answer
            answer = get_llm_answer(q, context_chunks)
            final_answers.append(answer)
            
        return final_answers
