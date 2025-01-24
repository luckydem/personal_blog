import json
import requests

API_KEY = "?key=AIzaSyDNm-LxK4dov5L4HMOM8ZBYuQkmDktfsJ0"

BASE_URL = "https://identitytoolkit.googleapis.com/v1/accounts"


def sign_in_with_email_and_password(email, password):
    
    print(f"sign_in_with_email_and_password({email}, {password})")
    
    request_type = ":signInWithPassword"
    url = f"{BASE_URL}{request_type}{API_KEY}"

    payload = { "email":email,"password":password,"returnSecureToken":"true" }
        
    response = requests.post(url=url, json=payload)
    
    if response.status_code not in [201, 200]:
        return response.text
    else:          
        return response.json()


# print(sign_in_with_email_and_password("demian@e-pod.app", "testing123"))


def sign_up_with_email_and_password(email, password):
    
    print(f"sign_up_with_email_and_password({email}, {password})")
    
    request_type = ":signUp"
    url = f"{BASE_URL}{request_type}{API_KEY}"
    
    payload = { "email": email, "password": password, "returnSecureToken":"true"}
    
    response = requests.post(url=url, json=payload)
    
    response_json = response.json()
    
    if response.status_code not in [201, 200]:
        response_error = response_json["error"]
        
        return f"Error: Code: {response_error["code"]}, Message: {response_error["message"]}"
    else:
        return response.json()
    
# print(sign_up_with_email_and_password(email="testing2@example.com", password="password123"))