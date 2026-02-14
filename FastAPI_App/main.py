from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class Student(BaseModel):
    name: str
    age: int
    course: str

@app.get("/")
def hello():
    return {"message": "Hello, World!"}

@app.post("/student")
def create_student(data: Student):
    return{
        "message": "Student created successfully",
        "student": data
    }

Users = {
    "1a": {"name": "Alice", "age": 21},
    "2b": {"name": "Bob", "age": 22},
    "3a": {"name": "Charlie", "age": 23},
}

@app.get("/user/{user_id}")
def get_user(user_id: str):
    user = Users.get(user_id)
    if user:
        return {"user_id": user_id, "user": user}
    return {"message": "User not found"}

@app.get("/users")
def get_all_users(user_id: str = None, is_all: bool = False):
    if user_id:
        user = Users.get(user_id)
        if user:
            return {"user_id": user_id, "user": user}
        return {"message": "User not found"}
    if is_all:
        return {"users": Users}
    return {"message": "No valid query parameters provided"}