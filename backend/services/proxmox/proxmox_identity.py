import requests
import urllib3
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from services.proxmox.proxmox_common import PROXMOX_HOST, PVE_HEADERS
#from proxmox_common import PROXMOX_HOST, PVE_HEADERS
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def proxmox_groups(name):
    group_url = f"{PROXMOX_HOST}/api2/json/access/groups"
    group_payload = {
        "groupid": name
    }
    group_response = requests.post(group_url, data=group_payload, headers=PVE_HEADERS, verify=False, timeout=10)
    return group_response.status_code

def group_details(group_info):
    # Fetch all groups in Proxmox
    proxmox_groups_url = f"{PROXMOX_HOST}/api2/json/access/groups"
    all_group_resp = requests.get(proxmox_groups_url, headers=PVE_HEADERS, verify=False, timeout=10)
    proxmox_groups_info = []
    for group in all_group_resp.json()["data"]:
        proxmox_groups_info.append(group["groupid"])
    print("Proxmox Groups")
    print(proxmox_groups_info)
    common_groups = set(group_info) & set(proxmox_groups_info)

    common_groups_info = []
    if common_groups:
        for group in common_groups:
            user_list = []
            group_permissions = []
            print(group)
            group_url = f"{PROXMOX_HOST}/api2/json/access/groups/{group}"
            group_response = requests.get(group_url, headers=PVE_HEADERS, verify=False, timeout=10)
            print(group_response.status_code)
            if group_response.status_code != 200:
                print(group_response.text)
            print(group_response.json()["data"]['members'])
            for member in group_response.json()["data"]['members']:
                if '@' in member:
                    user = member.split('@')[0]
                    if 'root' != user:
                        user_list.append(user)
            # Return Roles assigned to Group
            role_id_url = f"{PROXMOX_HOST}/api2/json/access/acl"
            role_id_response = requests.get(role_id_url, headers=PVE_HEADERS, verify=False, timeout=10)
            details = role_id_response.json()["data"]
            for information in details:
                if information["type"] == "group" and information["ugid"] == group:
                    group_permissions.append(information['roleid'])
            common_groups_info.append({
                "group_name": group,
                "users": user_list,
                "roles": group_permissions
            })
        print(common_groups_info)
        return common_groups_info
    else:
        return []

def delete_proxmox_groups(name):
    delete_group_url = f"{PROXMOX_HOST}/api2/json/access/groups/{name}"
    delete_group_response = requests.delete(delete_group_url,  headers=PVE_HEADERS, verify=False, timeout=10)
    print (delete_group_response.status_code)
    return delete_group_response.status_code











