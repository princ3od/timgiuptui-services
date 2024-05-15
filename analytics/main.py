from flask import Flask, Response
from models import User
from provider import Provider

app = Flask(__name__)

provider = Provider()


@app.get("/")
def health():
    return "OK", 200



@app.get("/users/{user_id}")
def get_user(user_id: int):
    user = provider.get(user_id)
    if user is None:
        return {"message": "User not found"}, 404
    return user


@app.post("/users")
def create_user(user: User):
    _user = provider.get(user.id)
    if _user is not None:
        return {"message": "User already exists"}, 409
    return provider.create(user), 201


@app.put("/users/{user_id}")
def update_user(user_id: int, user: User):
    _user = provider.get(user_id)
    if _user is None:
        return {"message": "Error user not existed"}, 404
    return provider.update(user_id, user), 200


@app.delete("/users/{user_id}")
def delete_user(user_id: int):
    user = provider.get(user_id)
    if user is None:
        return {"message": "Error"}, 404
    provider.delete(user_id)
    return Response(status=204)
