from pydantic import BaseModel
from typing import Union, Dict, List
from typing import Optional

# To validate and store data inputted by user from frontend
class createGroupRequest(BaseModel):
    group: str

class createGroupResponse(BaseModel):
    status_code: int
    message: str | None

class GroupDetails(BaseModel):
    group_name: str
    users: List[str]
    roles: List[str]


# 🔹 Full response schema
class getGroupResponse(BaseModel):
    group_details: List[GroupDetails]

class deleteGroupRequest(BaseModel):
    group: str

class deleteGroupResponse(BaseModel):
    status_code: int
    message: str | None
