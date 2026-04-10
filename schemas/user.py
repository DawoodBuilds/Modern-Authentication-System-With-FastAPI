from pydantic import BaseModel, Field, SecretStr, EmailStr, field_validator
from typing import Annotated
import re

class UserCreate(BaseModel):
    first_name: Annotated[str, Field(min_length=3, max_length=50, examples=["David"], alias="First Name")]
    last_name: Annotated[str, Field(min_length=3, max_length=50, examples=["Hussain"], alias="Last Name")]
    username: Annotated[str, Field(min_length=3, max_length=50, examples=["David786"])]
    email: Annotated[EmailStr, Field(min_length=5, max_length=100, examples=["example@gmail.com"])]
    password: Annotated[SecretStr, Field(min_length=8)]
    address: Annotated[str, Field()] = ""
    phone: Annotated[str, Field()] = ""

    @field_validator("password", mode="after")
    @classmethod
    def validate_password(cls, v: SecretStr) -> SecretStr:
        password = v.get_secret_value()
        if not re.search(r"[a-z]", password):
            raise ValueError("Password must contain at least one lowercase letter")
        if not re.search(r"[A-Z]", password):
            raise ValueError("Password must contain at least one uppercase letter")
        if not re.search(r"\d", password):
            raise ValueError("Password must contain at least one digit")
        if not re.search(r"[@$!%*?&]", password):
            raise ValueError("Password must contain at least one special character (@$!%*?&)")
        return v
    
    @field_validator("username", mode="after")
    @classmethod
    def username_lower(cls, username: str) -> str:
        return username.lower()
