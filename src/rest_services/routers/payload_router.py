import asyncio

from fastapi import APIRouter, HTTPException

from ..models.schemas import PayloadRequest, PayloadResponse

router = APIRouter()


@router.post("/payload", response_model=PayloadResponse)
async def process_large_payload(request: PayloadRequest):
    try:
        await asyncio.sleep(0.02 * (request.size_kb / 1024))
        response = PayloadResponse(
            success=True,
            processed_size_kb=request.size_kb,
        )

        return response
    except Exception as e:

        raise HTTPException(status_code=500, detail=str(e))
