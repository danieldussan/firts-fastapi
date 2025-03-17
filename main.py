from const import API_KEY
from fastapi import Depends, FastAPI, Header, HTTPException
from fastapi.staticfiles import StaticFiles
from routers import auth_jwt, products, users, users_db


def verify_api_key(x_api_key: str = Header(...)):
    if x_api_key != API_KEY:
        raise HTTPException(status_code=403, detail="Access denied")


app = FastAPI(dependencies=[Depends(verify_api_key)])

app.include_router(products.router)
app.include_router(users.router)
app.include_router(auth_jwt.router)
app.include_router(users_db.router)
app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/")
async def root():
    return {"message": "Hello FastApi"}
