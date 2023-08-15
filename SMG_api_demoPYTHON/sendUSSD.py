import requests
from concurrent.futures import ThreadPoolExecutor

# Set the base URL for the SMG Wireless Gateway API
base_url = " http://GateWayIP/API/SendUSSD"

# Set the authentication parameters
auth = {
    "username": "<USERNAME>",
    "password": "<PASSWORD>"
}

# Set the port numbers and USSD codes
ports = [1, 2, 3, 4]
ussd_codes = ["*123#", "*456#", "*789#", "*012#"]

def send_ussd(port, ussd_code):
    # Create the URL for sending a USSD request
    url = f"{base_url}/port/{port}/ussd"
    payload = {"event":"txssd", "port":port, "ussd":ussd_code}

    # Set the request data
    data = {
        "event":"txssd", 
        "port":port, 
        "ussd":ussd_code
    }

    # Send a POST request to the SMG Wireless Gateway API
    response = requests.post(url, json=data, auth=(auth["username"], auth["password"]))

    # Check if the request was successful
    if response.status_code == 200:
        # Get the USSD response from the response
        ussd_response = response.json()["ussd_response"]
        
        # Return the USSD response
        return ussd_response
    else:
        # Return an error message
        return f"Error: {response.status_code}"

# Create a ThreadPoolExecutor to execute requests concurrently
with ThreadPoolExecutor() as executor:
    # Submit tasks to send USSD requests for each port
    futures = [executor.submit(send_ussd, port, ussd_code) for port, ussd_code in zip(ports, ussd_codes)]
    
    # Wait for all tasks to complete and get their results
    ussd_responses = [future.result() for future in futures]
    
    # Print the USSD responses
    for port, ussd_response in zip(ports, ussd_responses):
        print(f"Port {port} USSD response: {ussd_response}")