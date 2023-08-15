import requests
from concurrent.futures import ThreadPoolExecutor

base_url = " http://GateWayIP/API/SendSMS"
auth = {
    "username": "<USERNAME>",
    "password": "<PASSWORD>"
}
# give values of userid, num and ports FIRST
userid = ""
num = []
ports = [] 
messages = ["Hello!", "How are you?", "Good morning!", "Have a nice day!"]
def send_sms_concurrently(base_url, auth, ports, messages):
    def send_sms(port, message):
        # Create the URL for sending an SMS message
        url = f"{base_url}/port/{port}/sms"

        # Set the request data
        data = {
            "event":"txms",
            "userid": "userid",
            "num":num,
            "port":ports,
            "encoding": "0",
            "smsinfo" : message
        }

        # Send a POST request to the SMG Wireless Gateway API
        response = requests.post(url, json=data, auth=(auth["username"], auth["password"]))

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
        # Submit tasks to send SMS messages for each port
        futures = [executor.submit(send_sms, port, message) for port, message in zip(ports, messages)]
        
        # Wait for all tasks to complete and get their results
        results = [future.result() for future in futures]
        
        # Print the results
        for port, result in zip(ports, results):
            print(f"Port {port} send SMS result: {result}")
