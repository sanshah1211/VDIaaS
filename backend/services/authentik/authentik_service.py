import requests
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from services.authentik import authentik_common as c


def create_authentik_user(user):
    payload = {
        "username": user.username,
        "email": user.email,
        "name": user.name,
        "is_active": True,
        "type": "internal"
    }
    auth_user_endpoint = f"{c.AUTHENTIK_HOST}/api/v3/core/users/"
    user_r = requests.post(auth_user_endpoint, headers=c.AUTHENTIK_HEADER, verify=False, json=payload, timeout=12)
    user_result = user_r.status_code

    if user_result == 201:
        id = user_r.json()["pk"]
        auth_password_endpoint = f"{c.AUTHENTIK_HOST}/api/v3/core/users/{id}/set_password/"
        password_payload = {
            "password": user.password
        }
        pass_r = requests.post(auth_password_endpoint, headers=c.AUTHENTIK_HEADER, verify=False, json=password_payload, timeout=12)
        pass_result = pass_r.status_code
        if pass_result == 204 :
            return "User Created Successfully"
        else:
            return pass_r.text
    else:
        return user_r.text

#user_list = {"username": "sanyams", "email": "shah.mhaswadkar@gmail.com", "name": "Sanyam Shah", "password": "Password@123"}
#print(create_authentik_user(user_list))

def authentik_user_login(user):
    url = f"{c.AUTHENTIK_HOST}/api/v3/flows/executor/default-authentication-flow/"
    session = requests.Session()
    # Start flow
    user_session = session.get(url)
    print("Stage 1:", user_session.json())
    # Identification stage
    payload = {
        "component": "ak-stage-identification",
        "uid_field": user.username
    }
    user_session = session.post(url, json=payload)
    print("Stage 2:", user_session.json())
    # Password stage
    payload = {
        "component": "ak-stage-password",
        "password": user.password
    }
    user_session = session.post(url, json=payload)
    print("Stage 3:", user_session.json())
    session_cookie = session.cookies.get("authentik_session")
    print("Session cookie:", session.cookies.get("authentik_session"))

    logged_in_url = f"{c.AUTHENTIK_HOST}/api/v3/core/users/me/"

    user_session = session.get(logged_in_url)

    if user_session.status_code == 200:
        return {
            "message": "Login Success",
            "cookie": session_cookie
        }
    else:
        return "Login Failed"