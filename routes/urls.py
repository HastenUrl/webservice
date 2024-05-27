from fastapi import APIRouter

router = APIRouter()

@router.get("/generate")
def generate_url():
    return {}