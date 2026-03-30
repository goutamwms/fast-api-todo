from pydantic import BaseModel, Field, EmailStr, ValidationInfo, field_validator


class Login(BaseModel):
    email: str = EmailStr
    password: str = Field(max_length=128, min_length=6)


class Register(BaseModel):
    name: str = Field(max_length=50, min_length=2)
    email: str = EmailStr
    password: str = Field(max_length=128, min_length=6)
    confirm_password: str = Field(max_length=128, min_length=6)

    @field_validator("confirm_password", mode="after")
    @classmethod
    def password_match(cls, v, info: ValidationInfo):
        if "password" in info.data and v != info.data["password"]:
            raise ValueError("Passwords do not match")
        return v


class AuthUser(BaseModel):
    id: int
    name: str
    email: EmailStr
