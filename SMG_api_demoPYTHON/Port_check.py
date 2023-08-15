import requests
from concurrent.futures import ThreadPoolExecutor

# Set the base URL for the SMG Wireless Gateway API
base_url = "http://GateWayIP/API/QueryPortInfo"

# Set the authentication parameters
auth = {
    "username": "<USERNAME>",
    "password": "<PASSWORD>"
}

# Set the port numbers
ports = [1, 2, 3, 4]

def get_port_status(port):
    # Create the URL for obtaining the port status
    url = f"{base_url}/port/{port}/status"
    # payload = "{\n    \"event\": \"getportinfo\"\n}"
    data = {
        "event":"getportinfo" 
    }

    # Send a GET request to the SMG Wireless Gateway API
    response = requests.get(url, json=data, auth=(auth["username"], auth["password"]))

    # Check if the request was successful
    if response.status_code == 200:
        # Get the port status from the response
        port_status = response.json()["port_status"]
        
        # Return the port status
        return port_status
    else:
        # Return an error message
        return f"Error: {response.status_code}"

# Create a ThreadPoolExecutor to execute requests concurrently
with ThreadPoolExecutor() as executor:
    # Submit tasks to obtain the port status for each port
    futures = [executor.submit(get_port_status, port) for port in ports]
    
    # Wait for all tasks to complete and get their results
    port_statuses = [future.result() for future in futures]
    
    # Print the port statuses
    for port, port_status in zip(ports, port_statuses):
        print(f"Port {port} status: {port_status}")
