from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from schemas.schemas import UserBasic, UserDbBasic

# Es una autención muy simple, no hace parte del router, solo es para el ejemplo
app = FastAPI()

oauth2 = OAuth2PasswordBearer(tokenUrl="login")


users_db = {
    "admin": {
        "username": "admin",
        "email": "admin@example.com",
        "disabled": False,
        "password": "admin",
    },
    "daniel": {
        "username": "daniel",
        "email": "daniel@example.com",
        "disabled": True,
        "password": "daniel",
    },
}


def search_user(username: str):
    if username in users_db:
        return UserBasic(**users_db[username])


def search_user_db(username: str):
    if username in users_db:
        return UserDbBasic(**users_db[username])


async def current_user(token: str = Depends(oauth2)):
    user = search_user(token)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    if user.disabled:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="User is disabled"
        )
    return user


@app.get("/user/me")
async def me(user: UserBasic = Depends(current_user)):
    return user


@app.post("/login")
async def login(form: OAuth2PasswordRequestForm = Depends()):
    user_db = search_user_db(form.username)

    if not user_db:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Incorrect username"
        )

    if not form.password == user_db.password:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Incorrect password"
        )

    return {"access_token": user_db.username, "token_type": "bearer"}
