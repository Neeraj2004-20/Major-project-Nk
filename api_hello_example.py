from fastapi import APIRouter

router = APIRouter()

@router.get("/hello", tags=["Demo"], include_in_schema=False)
def hello():
    return {"message": "Hello, world!"}