from fastapi import FastAPI, Depends
from pydantic import BaseModel
from models.student import Student

from db.deps import get_db
app = FastAPI()

class StudentRequestSchema(BaseModel):
    name: str
    age: int
    course: str

class StudentUpdateSchema(BaseModel):
    name: str = None
    age: int = None
    course: str = None

@app.get("/")
def hello_folks():
    return {"message": "Hello, folks! from FastAPI for Day 2"}

@app.post("/student")
def create_student(data: StudentRequestSchema, db = Depends(get_db) ):
    new_student = Student(
        name = data.name,
        age = data.age,
        course = data.course
    )

    db.add(new_student)
    db.commit()
    db.refresh(new_student)

    return new_student

@app.get("/students")
def get_all_students(id: int = None, db = Depends(get_db)):
    students = db.query(Student).all()
    if id:
        student = db.query(Student).filter(Student.id == id).first()
        if student:
            return student
        return {"message": "Student not found"}
    return students

@app.delete("/student")
def delete_student(id: int, db = Depends(get_db)):
    stu = db.query(Student).filter(Student.id == id).first()
    if not stu:
        return {"message": "Student not found"}
    db.delete(stu)
    db.commit()
    return {"message": "Student deleted successfully"}

@app.put("/student/{id}")
def update_student(id: int, data: StudentRequestSchema, db = Depends(get_db)):
    stu = db.query(Student).filter(Student.id == id).first()
    if not stu:
        return {"message": "Student not found"}
    
    stu.name = data.name
    stu.age = data.age
    stu.course = data.course
    db.commit()
    db.refresh(stu) # to update the data on python side from database side
    return stu

@app.patch("/student/{id}")
def update_student_partial(id: int, data: StudentUpdateSchema, db = Depends(get_db)):
    stu = db.query(Student).filter(Student.id == id).first()
    if not stu:
        return {"message": "Student not found"}
    
    # only update the fields which are provided in request(data)
    if data.name:
        stu.name = data.name
    if data.age:
        stu.age = data.age
    if data.course:
        stu.course = data.course

    db.commit()
    db.refresh(stu) # to update the data on python side from database side
    return stu
