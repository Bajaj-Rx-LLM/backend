import requests
import fitz  # PyMuPDF
from langchain.text_splitter import RecursiveCharacterTextSplitter

class DocumentProcessor:
    """
    Handles downloading, parsing, and chunking of PDF documents.
    """
    def __init__(self):
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1200,
            chunk_overlap=200
        )
        # Define a standard browser User-Agent header
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }

    def process_pdf_from_url(self, url: str) -> list[str]:
        """
        Downloads a PDF from a URL, extracts its text, and splits it into chunks.
        """
        try:
            print(f"Downloading document from: {url}")
            # Add the headers to the request to mimic a browser
            response = requests.get(url, headers=self.headers, timeout=20)
            response.raise_for_status()  # Raise an exception for bad status codes

            # Open PDF from in-memory content
            pdf_document = fitz.open(stream=response.content, filetype="pdf")
            
            full_text = ""
            for page in pdf_document:
                full_text += page.get_text()
            
            pdf_document.close()
            
            print("Document downloaded. Splitting into chunks...")
            chunks = self.text_splitter.split_text(full_text)
            return chunks

        except requests.exceptions.RequestException as e:
            print(f"❌ Error downloading PDF: {e}")
            return []
        except Exception as e:
            print(f"❌ Error processing PDF: {e}")
            return []
