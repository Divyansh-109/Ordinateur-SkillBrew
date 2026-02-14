# from fastapi import Depends
from db.config import sessionLocal

# generator function
# generator functions returns continous values using yield keyword
def get_db():
    db = sessionLocal()
    try:
        yield db
    finally:
        db.close()