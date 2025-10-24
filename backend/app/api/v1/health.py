from fastapi import APIRouter

router = APIRouter()

@router.get("/healthz")
def healthz():
    # keep original contract
    return {"ok": True}
