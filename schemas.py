from  pydantic import BaseModel
from typing import Optional



class Signup(BaseModel):
    
    username : str
    email : str
    password : str
    is_active : Optional[bool]
    is_staff : Optional[bool]


    class  Config:
        orm_mode = True
        schema_extra = {
            'example':{
                "username":"johndoe",
                "email":"johndoe@gmail.com",
                "password":"pass",
                "is_staff":False,
                "is_active":True
            }
        }


class Settings(BaseModel):
    authjwt_secret_key : str = 'ce29cffdea55bdba8012ff9033ec959b0c7870aa03e11146db34b0aaf6183a96'


class LoginModel(BaseModel):
    username: str
    password: str





class OrderModel(BaseModel):
    id : Optional[int]
    quantity : int
    order_status : Optional[str]="PENDING"
    pizza_size : Optional[str]="SMALL"
    user_id : Optional[int]

    class config:
        orm_mode = True
        schema_extra={
            "example":{
                "quantity":2,
                "pizza_size":"LARGE"
            }
        }



