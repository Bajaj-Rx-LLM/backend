import hashlib
from pydantic import HttpUrl

def create_document_id(url: HttpUrl) -> str:
    """
    Creates a unique and consistent SHA256 hash from a URL to use as a document ID.
    This acts as our cache key.
    """
    # Convert the HttpUrl object to a string before encoding
    return hashlib.sha256(str(url).encode()).hexdigest()
