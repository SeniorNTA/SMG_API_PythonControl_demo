import requests
from concurrent.futures import ThreadPoolExecutor

# Set the base URL for the SMG Wireless Gateway API
base_url = " http://GateWayIP/API/SwitchCard"

# Set the authentication parameters
auth = {
    "username": "<USERNAME>",
    "password": "<PASSWORD>"
}

# Set the port numbers and SIM card slots
ports = [1, 2, 3, 4]
sim_slots = [1, 2, 1, 2]

def switch_sim(port, sim_slot):
    # Create the URL for switching the SIM card
    url = f"{base_url}/port/{port}/sim/{sim_slot}"
    data = {
        "event":"switchcard", 
        "port":port, 
        # "sim_slot":
    }

    # Send a POST request to the SMG Wireless Gateway API
    response = requests.post(url, auth=(auth["username"], auth["password"]))

    # Check if the request was successful
    if response.status_code == 200:
        # Get the result from the response
        result = response.json()["result"]
        
        # Return the result
        return result
    else:
        # Return an error message
        return f"Error: {response.status_code}"

# Create a ThreadPoolExecutor to execute requests concurrently
with ThreadPoolExecutor() as executor:
    # Submit tasks to switch the SIM card for each port
    futures = [executor.submit(switch_sim, port, sim_slot) for port, sim_slot in zip(ports, sim_slots)]
    
    # Wait for all tasks to complete and get their results
    results = [future.result() for future in futures]
    
    # Print the results
    for port, result in zip(ports, results):
        print(f"Port {port} switch SIM result: {result}")
