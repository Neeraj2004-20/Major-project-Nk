from fastapi import APIRouter

router = APIRouter()

@router.get("/info", tags=["Demo"], include_in_schema=True)
def info():
    return {
        "app": "AI Market Predictor",
        "version": "1.0",
        "status": "running"
    }
