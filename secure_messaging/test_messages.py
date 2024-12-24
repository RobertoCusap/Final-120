# test_messages.py
import requests
import json
import time

def send_message(content):
    sender_url = "http://localhost:8000/api/messages/"
    data = {
        "content": content,
        "recipient_url": "http://localhost:8001/api/received-messages/"
    }
    
    print(f"\nSending message: {content}")
    response = requests.post(sender_url, json=data)
    print(f"Sender Response Status: {response.status_code}")
    print("Sender Response Data:", json.dumps(response.json(), indent=2))
    return response.json()

def get_received_messages():
    receiver_url = "http://localhost:8001/api/received-messages/"
    response = requests.get(receiver_url)
    print("\nReceived Messages:")
    print(json.dumps(response.json(), indent=2))
    return response.json()

def run_tests():
    # Test 1: Send a simple message
    print("\n=== Test 1: Sending Simple Message ===")
    send_message("Hello, this is a test message!")
    time.sleep(1)  # Wait for processing
    get_received_messages()

    # # Test 2: Send a message with special characters
    # print("\n=== Test 2: Sending Message with Special Characters ===")
    # send_message("Testing £€$@ characters and emojis 👋🌟!")
    # time.sleep(1)
    # get_received_messages()

    # # Test 3: Send a longer message
    # print("\n=== Test 3: Sending Longer Message ===")
    # send_message("This is a longer message that tests the system's ability to handle multiple sentences. It includes various punctuation marks and symbols! How will it handle this?")
    # time.sleep(1)
    # get_received_messages()

if __name__ == "__main__":
    run_tests()