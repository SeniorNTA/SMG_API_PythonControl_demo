import requests
import json
from concurrent.futures import ThreadPoolExecutor

# Set the base URL for the SMG Wireless Gateway API
base_url = "http://GateWayIP/API"

# Set the authentication credentials
auth = ("API_account", "API_password")

# Set the request parameters
params = {
    "event": "txsms",
    "userid": "0",
    "num":".....",
    "port": "ex: 1,2,3",
    "encoding": "0",
    "smsinfo": "Hello, this is a test message!"
    # "port": 1
}

def call_api():
    # Send the request to the SMG Wireless Gateway API
    response = requests.post(f"{base_url}/SendSmS", auth=auth, data=json.dumps(params))

    # Check if the request was successful
    if response.status_code == 200:
        # Parse the response JSON
        response_json = response.json()
        
        # Check if the result was successful
        if response_json["result"] == "ok":
            # Print the content of the response
            print(response_json["content"])
        else:
            # Print the error message
            print(f"Error: {response_json['content']}")
    else:
        # Print an error message
        print(f"Error: Request failed with status code {response.status_code}")

# Create a ThreadPoolExecutor with 5 worker threads
with ThreadPoolExecutor(max_workers=5) as executor:
    # Submit 5 tasks to call the SMG Wireless Gateway API concurrently
    for _ in range(5):
        executor.submit(call_api)
