import requests
from concurrent.futures import ThreadPoolExecutor

def check_sim_slots_concurrently(base_url, auth, ports):
    def check_sim_slots(port):
        # Create the URL for checking the available SIM slots
        url = f"{base_url}/port/{port}/sim"

        # Send a GET request to the SMG Wireless Gateway API
        response = requests.get(url, auth=(auth["username"], auth["password"]))

        # Check if the request was successful
        if response.status_code == 200:
            # Get the available SIM slots from the response
            sim_slots = response.json()["sim_slots"]
            
            # Return the available SIM slots
            return sim_slots
        else:
            # Return an error message
            return f"Error: {response.status_code}"

    # Create a ThreadPoolExecutor to execute requests concurrently
    with ThreadPoolExecutor() as executor:
        # Submit tasks to check the available SIM slots for each port
        futures = [executor.submit(check_sim_slots, port) for port in ports]
        
        # Wait for all tasks to complete and get their results
        sim_slots_list = [future.result() for future in futures]
        
        # Print the available SIM slots
        for port, sim_slots in zip(ports, sim_slots_list):
            print(f"Port {port} available SIM slots: {sim_slots}")

# Example usage of the function
base_url = "http://<SMG_IP>/api/smg"
auth = {
    "username": "<USERNAME>",
    "password": "<PASSWORD>"
}
ports = [1, 2, 3, 4]

check_sim_slots_concurrently(base_url, auth, ports)
