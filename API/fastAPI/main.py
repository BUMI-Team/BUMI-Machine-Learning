from uuid import uuid4
from fastapi import FastAPI
from models import *

app = FastAPI()

db : List[User] = [
    User(
        id = uuid4(), 
        first_name="nur",
        last_name="nur",
        middle_name="nur",
        gender=Gender.female,
        roles = [Role.student]
    ),
    User(
        id = uuid4(), 
        first_name="ilmi",
        last_name="ilmmi",
        middle_name="ilmi",
        gender=Gender.female,
        roles = [Role.admin, Role.user]
    )
]


@app.get("/")
def root():
    return {"message": "Hello World"}

@app.get("/api/v1/users")
async def fetch_users():
    return db;

@app.post("/api/v1/users")
async def register_user(user: User):
    db.append(user)
    return {"id": user.id}

@app.delete("/api/v1/users/{user_id}")
async def delete_user(user_id: UUID):
    for user in db:
        if user.id == user_id:
            db.remove(user_id)
            return

@app.put("/api/v1/users/{user_id}")
async def update_user(user_update: UserUpdateRequest, user_id: UUID):
    for user in db:
        if user.id == user_id:
            if user_update.first_name is not None:
                user.first_name = user_update.first_name
            if user_update.last_name is not None:
                user.last_name = user_update.last_name
            if user_update.middle_name is not None:
                user.middle_name = user_update.middle_name
            if user_update.roles is not None:
                user.roles = user_update.roles
            return