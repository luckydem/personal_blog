from flask import request
from google.auth.transport import requests as google_auth_requests
from google.oauth2 import id_token as google_id_token
from .models import retrieve_user


def userSignedIn():
    print("app/helpers.py --> userSignedIn()")
    
    firebase_request_adapter = google_auth_requests.Request()
    id_token = request.cookies.get("token")
    
    # print(f"id_token: {id_token}")
    
    error_message = None
    claims = None
    authenticated = False
    
    if id_token:        
        try:
            claims = google_id_token.verify_firebase_token(
                id_token, firebase_request_adapter
            )
            
            authenticated = retrieve_user(claims.get('user_id'))
                                            
        except ValueError as exc:
            error_message = str(exc)   
    
    # print(f"authenticated: {authenticated}")
    
            
    return {"error_message": error_message, "claims" : claims, "authenticated": authenticated}