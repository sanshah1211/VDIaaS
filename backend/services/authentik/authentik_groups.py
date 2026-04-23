import requests
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from services.authentik.authentik_common import AUTHENTIK_HEADER, AUTHENTIK_HOST, AUTHENTIK_API_TOKEN, PG_PASSWORD

def create_authentik_groups(name):
    group_url = f"{AUTHENTIK_HOST}/api/v3/core/groups/"
    group_payload = {
        "name": name
    }
    group_response = requests.post(group_url, headers=AUTHENTIK_HEADER, json=group_payload, verify=False, timeout=10)
    print(group_response.json())
    return group_response.status_code
#create_authentik_groups()

def get_authentik_groups():
    group_details = []
    group_url = f"{AUTHENTIK_HOST}/api/v3/core/groups/"
    group_response = requests.get(group_url, headers=AUTHENTIK_HEADER, verify=False, timeout=10)
    for r in group_response.json()["results"]:
        group_details.append(
            {
                "name": r["name"],
                "uuid": r["pk"]
            }
        )
    return group_details
#print(get_authentik_groups())

def delete_authentik_groups(name):
    group_details = get_authentik_groups()
    for group in group_details:
        if group["name"] == name:
            group_id = group["uuid"]
            delete_group_url = f"{AUTHENTIK_HOST}/api/v3/core/groups/{group_id}/"
            delete_group_response = requests.delete(delete_group_url, headers=AUTHENTIK_HEADER, verify=False, timeout=10)
            return delete_group_response.status_code

