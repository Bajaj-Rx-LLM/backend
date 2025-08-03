import requests
import json

# --- Configuration ---
# This should be the URL of your locally running FastAPI app
API_ENDPOINT = "http://localhost:8001/ingest" # Changed to port 8001

# This is the secret key you defined in api/routes.py
API_KEY = "your_secret_api_key_here" 

# This is a sample PDF URL you can use for testing
TEST_PDF_URL = "https://bitcoin.org/bitcoin.pdf"

# --- Prepare the request ---
headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

# The /ingest endpoint only needs the 'documents' field, 
# but we send 'questions' to match the Pydantic model.
payload = {
    "documents": TEST_PDF_URL,
    "questions": [] 
}

# --- Send the request ---
print(f"🚀 Sending POST request to test ingestion at {API_ENDPOINT}...")

try:
    response = requests.post(API_ENDPOINT, headers=headers, data=json.dumps(payload), timeout=60)
    
    # Raise an exception if the request returned an error code
    response.raise_for_status() 
    
    print("\n✅ Ingestion request successful!")
    print(f"Status Code: {response.status_code}")
    print("\n--- Response from API ---")
    print(response.json())

except requests.exceptions.HTTPError as http_err:
    print(f"❌ HTTP error occurred: {http_err}")
    print(f"Response Body: {response.text}")
except requests.exceptions.RequestException as err:
    print(f"❌ An error occurred: {err}")
