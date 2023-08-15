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

def get_sim_status(port):
    # Create the URL for obtaining the port SIM status
    url = f"{base_url}/port/{port}/sim"
    # payload = "{\n    \"event\": \"getportinfoex\"\n}"
    data = {
        "event":"getportinfoex" 
    }
    # Send a GET request to the SMG Wireless Gateway API
    response = requests.get(url, json=data, auth=(auth["username"], auth["password"]))

    # Check if the request was successful
    if response.status_code == 200:
        # Get the port SIM status from the response
        sim_status = response.json()["sim_status"]
        
        # Return the port SIM status
        return sim_status
    else:
        # Return an error message
        return f"Error: {response.status_code}"

# Create a ThreadPoolExecutor to execute requests concurrently
with ThreadPoolExecutor() as executor:
    # Submit tasks to obtain the port SIM status for each port
    futures = [executor.submit(get_sim_status, port) for port in ports]
    
    # Wait for all tasks to complete and get their results
    sim_statuses = [future.result() for future in futures]
    
    # Print the port SIM statuses
    for port, sim_status in zip(ports, sim_statuses):
        print(f"Port {port} SIM status: {sim_status}")