import requests
import json

url = "http://localhost:11434/api/generate"
payload = {
    "model": "llama2:latest",
    "prompt": "Hi, tell me a short joke.",
    "stream": False
}

try:
    print(f"Connecting to {url}...")
    response = requests.post(url, json=payload, timeout=30)
    print(f"Status: {response.status_code}")
    print(f"Response: {response.text}")
except Exception as e:
    print(f"Error: {str(e)}")
