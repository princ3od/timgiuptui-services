from fastapi import FastAPI, status, HTTPException

from provider import Provider
from models import User

app = FastAPI(version="0.1.0", title="FastAPI", description="FastAPI example")

provider = Provider()


@app.get("/", status_code=status.HTTP_200_OK)
def health():
    return "OK"


@app.get("/users/{user_id}", status_code=status.HTTP_200_OK)
def get_user(user_id: int):
    user = provider.get(user_id)
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user


@app.post("/users", status_code=status.HTTP_201_CREATED)
def create_user(user: User):
    _user = provider.get(user.id)
    if _user is not None:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="User already exists")
    return provider.create(user)


@app.put("/users/{user_id}", status_code=status.HTTP_200_OK)
def update_user(user_id: int, user: User):
    _user = provider.get(user_id)
    if _user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return provider.update(user_id, user)


@app.delete("/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_id: int):
    user = provider.get(user_id)
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    provider.delete(user_id)
