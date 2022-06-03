import os
import requests

BASE_URL = "https://webexapis.com/v1/"

def post_message(message, token=os.getenv("WEBEX_TOKEN"), roomid=os.getenv("WEBEX_ROOM")):
    '''
    A function to send a text based message to a Webex room.
    '''
    print(f"Sending message: {message}")
    url = f"{BASE_URL}messages"
    headers = {"authorization":f"Bearer {token}", "Content-Type":"application/json"}
    payload = {
        "roomId":roomid,
        "text":message
    }
    response = requests.post(url, headers=headers, json=payload)
    print(f"Status code of sending the Webex message: {response.status_code}")


if __name__ == "__main__":
    post_message("Hello Cisco Live :)")