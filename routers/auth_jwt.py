from datetime import datetime, timedelta

import jwt
from const import ACCESS_TOKEN_EXPIRE_TIME, ALGORITHM, JWT_SECRET_KEY
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from passlib.context import CryptContext
from schemas.schemas import UserBasic, UserDbBasic, responseToken

crypt = CryptContext(schemes=["bcrypt"])
oauth2 = OAuth2PasswordBearer(tokenUrl="login")


router = APIRouter(
    prefix="/auth",
    tags=["auth"],
    responses={404: {"message": "Not found"}},
)


users_db = {
    "admin": {
        "username": "admin",
        "email": "admin@example.com",
        "disabled": False,
        "password": "$2a$10$ajTr12PG0Pe6/k4m9Howg.PTAm94T6k3Df6W9tdHSrOLlRhnBkb4W",
    },
    "daniel": {
        "username": "daniel",
        "email": "daniel@example.com",
        "disabled": True,
        "password": "$2a$10$rLYg46BxHFuNfMYRxM2JPu8WZ0e9ApXYIo8.J4JFOhi7fFjyJ6KOC",
    },
}


def search_user(username: str):
    if username in users_db:
        return UserBasic(**users_db[username])


def search_user_db(username: str):
    if username in users_db:
        return UserDbBasic(**users_db[username])


async def auth_user(token: str = Depends(oauth2)):
    exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Incorrect credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        username = jwt.decode(token, JWT_SECRET_KEY, algorithms=[ALGORITHM]).get("sub")
        if username is None:
            raise exception

    except jwt.DecodeError:
        raise exception

    return search_user(username)


async def current_user(user: UserBasic = Depends(auth_user)):
    if user.disabled:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="User is disabled"
        )
    return user


@router.post("/login", response_model=responseToken)
async def login(form: OAuth2PasswordRequestForm = Depends()):
    user_db = search_user_db(form.username)

    if not user_db:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Incorrect username"
        )

    if not crypt.verify(form.password, user_db.password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Incorrect password"
        )
    access_token = {
        "sub": user_db.username,
        "exp": datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_TIME),
    }
    token = jwt.encode(access_token, JWT_SECRET_KEY, algorithm=ALGORITHM)

    return responseToken(access_token=token, token_type="bearer")


@router.get("/me")
async def me(user: UserBasic = Depends(current_user)):
    return user


@router.get("/data", dependencies=[Depends(current_user)])
async def test():
    return {"message": "Test para probar jwt"}
