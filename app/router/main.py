from fastapi import APIRouter

router = APIRouter()

@router.get("/api/")
async def root(token_id: int):
    """
    Return json with metadata
    """

    r = {
        "name": "Envelop API",
        "external_url": "https://app.envelop.is/",
    }
    return r