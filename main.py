from fastapi import FastAPI
from api import routes as api_routes

app = FastAPI(
    title="HackRx 6.0 Backend",
    description="API for processing documents and answering questions.",
    version="1.0.0"
)

# Include the router from the api module
app.include_router(api_routes.router)

@app.get("/", tags=["Health Check"])
def read_root():
    """A simple health check endpoint to confirm the server is running."""
    return {"status": "ok", "message": "Welcome to the HackRx API!"}

# To run this application:
# 1. Make sure your ChromaDB Docker container is running.
# 2. Install all dependencies: pip install fastapi uvicorn python-multipart "pydantic[email]" requests PyMuPDF langchain sentence-transformers chromadb
# 3. Run in your terminal: uvicorn main:app --host 0.0.0.0 --port 8000 --reload
