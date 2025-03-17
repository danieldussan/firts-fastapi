from typing import List, Union

from bson import ObjectId
from db.client import db_client
from db.models.user import User, User_body
from db.schemas.user import user_list_schema, user_schema
from fastapi import APIRouter, HTTPException


router = APIRouter(
    tags=["users db"], responses={404: {"message": "Not found"}}, prefix="/userdb"
)


@router.get("/", response_model=List[User])
async def get_users():
    try:
        users = user_list_schema(db_client.users.find())
    except:
        raise HTTPException(status_code=404, detail="Users not found")
    return users


@router.get("/{id}", response_model=Union[User, dict])
async def get_user_by(id: str):
    user = search_user("_id", ObjectId(id))
    return user


@router.post("/", response_model=User, status_code=201)
async def create_user(user: User_body):
    if type(search_user("email", user.email)) is User:
        raise HTTPException(status_code=400, detail="User already exists")
    user_dict = dict(user)
    del user_dict["id"]
    id = db_client.users.insert_one(user_dict).inserted_id
    new_user = search_user("_id", ObjectId(id))

    return new_user


@router.put("/", response_model=User, status_code=200)
async def update_user(user: User):
    if not ObjectId.is_valid(user.id):
        raise HTTPException(status_code=400, detail="Invalid user ID")

    user_id = ObjectId(user.id)
    user_db = db_client.users.find_one({"_id": user_id})
    if user_db is None:
        raise HTTPException(status_code=404, detail="User not found")

    user_dict = dict(user)
    del user_dict["id"]

    existing_user = search_user("email", user.email)
    if type(existing_user) is User:
        raise HTTPException(status_code=400, detail="Email already exists")

    try:
        data = db_client.users.update_one({"_id": user_id}, {"$set": user_dict})
        if data.matched_count == 0:
            raise HTTPException(status_code=404, detail="User update failed")

    except Exception:
        raise HTTPException(status_code=400, detail="Error updating user")

    return search_user("_id", user_id)


@router.delete("/{id}", status_code=200)
async def delete_user(id: str):
    found = db_client.users.find_one_and_delete({"_id": ObjectId(id)})

    if not found:
        raise HTTPException(status_code=404, detail="User not found")

    return {"message": "User deleted successfully"}


def search_user(key: str, value):
    try:
        user = user_schema(db_client.users.find_one({key: value}))
        return User(**user)
    except:
        return {"error": "User not found"}
