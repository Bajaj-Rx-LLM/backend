from fastapi import APIRouter, Depends, Header, HTTPException, status
from .models import HackRxRequest, HackRxResponse
from core.rag_service import RAGService
from core.document_processor import DocumentProcessor
from core.cache_manager import CacheManager
from utils.helpers import create_document_id

# A placeholder for your API key. In a real app, use environment variables.
API_KEY = "your_secret_api_key_here" 

router = APIRouter()

# --- Dependencies ---
def get_rag_service():
    return RAGService()

def get_doc_processor():
    return DocumentProcessor()

def get_cache_manager():
    return CacheManager()

async def verify_api_key(authorization: str = Header(...)):
    if authorization != f"Bearer {API_KEY}":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid Authorization Header",
        )

# --- Main Production Endpoint ---
@router.post(
    "/hackrx/run",
    response_model=HackRxResponse,
    dependencies=[Depends(verify_api_key)]
)
async def run_hackrx_pipeline(
    request: HackRxRequest,
    rag_service: RAGService = Depends(get_rag_service)
):
    """
    The main endpoint for the HackRx challenge.
    It receives a document URL and questions, processes them, and returns answers.
    """
    try:
        answers = rag_service.process_request(request)
        return HackRxResponse(answers=answers)
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An internal error occurred while processing the request."
        )

# --- New Testing Endpoint ---
@router.post(
    "/ingest",
    tags=["Testing"],
    dependencies=[Depends(verify_api_key)]
)
async def ingest_document(
    request: HackRxRequest, # We reuse the model, but will ignore the 'questions' field
    processor: DocumentProcessor = Depends(get_doc_processor),
    cache: CacheManager = Depends(get_cache_manager)
):
    """
    A testing endpoint to ONLY process and cache a document.
    It does not call the LLM or answer questions.
    """
    doc_url = request.documents
    doc_id = create_document_id(doc_url)

    if cache.check_if_processed(doc_id):
        return {"status": "skipped", "message": f"Document {doc_id} is already in the cache."}

    print(f"Starting ingestion for document: {doc_id}")
    chunks = processor.process_pdf_from_url(doc_url)
    
    if not chunks:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Failed to process document from the provided URL."
        )
    
    cache.add_to_cache(doc_id, chunks)
    
    return {"status": "success", "doc_id": doc_id, "chunks_ingested": len(chunks)}
