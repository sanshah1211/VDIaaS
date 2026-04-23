from fastapi import APIRouter
from schemas.user_schemas import userSignUpRequest, userSignUpResponse, userLoginResponse, userLoginRequest
from services.authentik.authentik_service import create_authentik_user, authentik_user_login
from schemas.group_schemas import createGroupRequest, createGroupResponse, getGroupResponse, deleteGroupRequest, deleteGroupResponse
from services.authentik.authentik_groups import create_authentik_groups, get_authentik_groups, delete_authentik_groups
from services.proxmox.proxmox_identity import proxmox_groups, group_details, delete_proxmox_groups


router = APIRouter()

@router.post("/signup", response_model=userSignUpResponse)
def sign_up(user: userSignUpRequest):
    result =  create_authentik_user(user)
    return({
        "message": result
    })

@router.post("/", response_model=userLoginResponse)
def login(user: userLoginRequest):
    result =  authentik_user_login(user)
    return({
        "message": result["message"],
        "cookie": result["cookie"]
    })

@router.post("/create-groups", response_model=createGroupResponse)
def create_groups(group: createGroupRequest):
    group_name = group.group
    print(group_name)
    authentik_result = create_authentik_groups(group_name)
    proxmox_result = proxmox_groups(group_name)
    if authentik_result == 201 and proxmox_result == 200:
        return ({
            "status_code": 200,
            "message": "Group Created"
        })
    return ({
        "status_code": 400,
        "message": "Failed"
    })

@router.get("/groups", response_model=getGroupResponse)
def get_groups():
    result = get_authentik_groups()
    group_info = []

    for group in result:
        group_info.append(
            group["name"]
        )

    print("Authentik Groups")
    print(group_info)
    proxmox_group_info = group_details(group_info)
    print("Common Groups")
    print(proxmox_group_info)

    if proxmox_group_info != None:
        return {
            "group_details": proxmox_group_info
        }

@router.delete("/delete-groups/{group_name}")
def delete_groups(group_name: str):
    print(group_name)
    authentik_result = delete_authentik_groups(group_name)
    proxmox_result = delete_proxmox_groups(group_name)
    print(proxmox_result)
    if authentik_result == 204 and proxmox_result == 200:
        return ({
            "status_code": 200,
            "message": "Group Deleted"
        })
    return ({
        "status_code": 400,
        "message": "Failed"
    })

