from fastapi import APIRouter, Depends
from app.models.auth import Register, Login
from typing import Annotated
from sqlalchemy.orm import Session
from app.database.db import get_db
from app.database.schema.user_schema import UserSchema
from fastapi.responses import JSONResponse
from app.helper import hashPassword, verifyPassword, createAccessToken

router = APIRouter(prefix="/auth")


@router.post("/register")
def register(data: Register, db: Annotated[Session, Depends(get_db)]):
    existing_user = db.query(UserSchema).filter(UserSchema.email == data.email).first()

    if existing_user:
        return JSONResponse({"message": "User already exists"}, status_code=400)

    new_user = UserSchema(
        name=data.name, email=data.email, password=hashPassword(data.password)
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"message": "User created", "data": new_user}


@router.post("/login")
def login(data: Login, db: Annotated[Session, Depends(get_db)]):
    user = db.query(UserSchema).filter(UserSchema.email == data.email).first()
    if not user or not verifyPassword(data.password, user.password):
        return JSONResponse({"message": "Invalid email or password"}, status_code=401)

    payload = {"id": user.id, "name": user.name, "email": user.email}

    token = createAccessToken(payload)
    payload["access_token"] = token

    return {"message": "Login success", "data": payload}
