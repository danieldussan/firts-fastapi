from typing import List, Union

from fastapi import APIRouter, HTTPException

from schemas.schemas import MessageResponse, User

user_list = [
    User(id=1, name="John", lastName="Doe", age=30),
    User(id=2, name="Jane", lastName="Doe", age=25),
    User(id=3, name="Peter", lastName="Jones", age=40),
]

router = APIRouter(tags=["users"], responses={404: {"message": "Not found"}})


@router.get("/users", response_model=List[User])
async def get_users():
    return user_list


# Get by Path
@router.get("/user_by_path/{id}", response_model=Union[User, dict])
async def get_user_by_path(id: int):
    return search_user(id)


# Get By Query http://localhost:8000/user_by_query?id=1
# @router.get("/user_by_query", response_model=User)
# async def get_user_by_query(id: int):
#     return search_user(id)


@router.post("/user", response_model=User, status_code=201)
async def create_user(user: User) -> User:
    if isinstance(search_user(user.id), User):
        raise HTTPException(status_code=400, detail="User already exists")

    user_list.append(user)
    return user


@router.put("/user", response_model=User, status_code=200)
async def update_user(user: User) -> User:
    for index, user_in_list in enumerate(user_list):
        if user_in_list.id == user.id:
            user_list[index] = user
            return user

    raise HTTPException(status_code=404, detail="User not found")


@router.delete("/user/{id}", response_model=MessageResponse, status_code=200)
async def delete_user(id: int) -> MessageResponse:
    for index, user_in_list in enumerate(user_list):
        if user_in_list.id == id:
            del user_list[index]
            return MessageResponse(message="User deleted successfully")

    raise HTTPException(status_code=404, detail="User not found")


def search_user(id: int) -> Union[User, None]:
    users = list(filter(lambda user: user.id == id, user_list))
    return users[0] if users else None
