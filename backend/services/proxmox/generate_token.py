import requests
import urllib3
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from proxmox_common import PROXMOX_HOST, PROXMOX_PASSWORD, PROXMOX_USER


urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def token_setup():
    login_request = f"{PROXMOX_HOST}/api2/json/access/ticket"
    payload = {
        "username": PROXMOX_USER,
        "password": PROXMOX_PASSWORD,
    }

    login_response = requests.post(login_request, data=payload, verify=False, timeout=5)
    data = login_response.json()['data']
    print(data)
    ticket = data["ticket"]
    print("Ticket:", ticket)
    csrf_token = data["CSRFPreventionToken"]
    print("Token:", csrf_token)

    headers = {
        "CSRFPreventionToken": csrf_token
    }
    print(headers)
    cookies = {
        "PVEAuthCookie": ticket
    }
    print(cookies)
    token_request_url = f"{PROXMOX_HOST}/api2/json/access/users/{PROXMOX_USER}/token/vdiaas"
    payload = {
        "privsep": 0
    }
    token_response = requests.post(token_request_url, data=payload, headers=headers, cookies=cookies, verify=False, timeout=5)
    data = token_response.json()["data"]
    print(data)
    PROXMOX_TOKEN_ID = data["full-tokenid"]
    print("PROXMOX_TOKEN_ID:", PROXMOX_TOKEN_ID)
    PROXMOX_TOKEN_SECRET = data["value"]
    print("PROXMOX_TOKEN_SECRET:", PROXMOX_TOKEN_SECRET)

    acl_url = f"{PROXMOX_HOST}/api2/json/access/acl"
    permission_payload = {
        "path": "/",
        "roles": "Administrator",
        "tokens": [PROXMOX_TOKEN_ID],
        "propagate": 1
    }

    acl_response = requests.put(acl_url, data=permission_payload, verify=False, headers=headers, cookies=cookies, timeout=5)
    print(acl_response.json())

    common_settings = "./proxmox_common.py"
    with open(common_settings, "r") as f:
        lines = f.readlines()

    with open(common_settings, "w") as f:
        for line in lines:
            if "Authorization" in line:
                f.write(f'"Authorization": "PVEAPIToken={PROXMOX_TOKEN_ID}={PROXMOX_TOKEN_SECRET}"\n')
            else:
                f.write(line)


token_setup()


