import requests
import json

# --- Configuration ---
# This should be the URL of your locally running FastAPI app
API_ENDPOINT = "http://localhost:8000/hackrx/run" 

# This is the secret key you defined in api/routes.py
API_KEY = "your_secret_api_key_here" 

# This is a sample PDF URL you can use for testing
TEST_PDF_URL = "https://images.chesscomfiles.com/images/web/docs/chess-rules.pdf"

# The questions you want to ask
TEST_QUESTIONS = [
    "How does a pawn move?",
    "What is castling?"
]

# --- Prepare the request ---
headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

payload = {
    "documents": TEST_PDF_URL,
    "questions": TEST_QUESTIONS
}

# --- Send the request ---
print(f"🚀 Sending POST request to {API_ENDPOINT}...")

try:
    response = requests.post(API_ENDPOINT, headers=headers, data=json.dumps(payload), timeout=60)
    
    # Raise an exception if the request returned an error code
    response.raise_for_status() 
    
    print("\n✅ Request successful!")
    print(f"Status Code: {response.status_code}")
    print("\n--- Response from API ---")
    print(json.dumps(response.json(), indent=2))

except requests.exceptions.HTTPError as http_err:
    print(f"❌ HTTP error occurred: {http_err}")
    print(f"Response Body: {response.text}")
except requests.exceptions.RequestException as err:
    print(f"❌ An error occurred: {err}")
