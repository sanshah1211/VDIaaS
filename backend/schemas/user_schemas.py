from pydantic import BaseModel
from typing import Union, Dict, List
from typing import Optional

# To validate and store data inputted by user from frontend
class userSignUpRequest(BaseModel):
    username: str
    email: str
    name: str
    password: str

class userSignUpResponse(BaseModel):
    message: Union[str, Dict[str, List[str]]]

class userLoginRequest(BaseModel):
    username: str
    password: str


class userLoginResponse(BaseModel):
    message: str
    cookie: Union[str, Dict[str, List[str]]] | None



