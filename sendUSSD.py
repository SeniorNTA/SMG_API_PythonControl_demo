import requests
import json
from concurrent.futures import ThreadPoolExecutor
import redis

# Set the base URL for the SMG Wireless Gateway API
base_url = "http://GateWayIP/API"

# Set the authentication credentials
auth = ("API_account", "API_password")

# Set the request parameters
params = {
    "event": "txussd",
    "port": 1,
    "content": "*101#"
}

# Connect to the Redis server
redis_client = redis.Redis()

def call_api():
    # Send the request to the SMG Wireless Gateway API
    response = requests.post(f"{base_url}/SendUssd", auth=auth, data=json.dumps(params))

    # Check if the request was successful
    if response.status_code == 200:
        # Parse the response JSON
        response_json = response.json()
        
        # Check if the result was successful
        if response_json["result"] == "ok":
            # Store the content of the response in Redis
            redis_client.set("ussd_response", json.dumps(response_json["content"]))
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
