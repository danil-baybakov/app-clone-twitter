from fastapi import APIRouter

router = APIRouter(redirect_slashes=False, tags=["root"])


@router.get("/")
async def root() -> dict[str, str]:
    return {"message": "Welcome to the Twitter clone app!"}
