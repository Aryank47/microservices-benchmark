import asyncio

from fastapi import APIRouter, HTTPException

from ..models.schemas import SimpleRequest, SimpleResponse

router = APIRouter()


@router.post("/simple", response_model=SimpleResponse)
async def process_request(request: SimpleRequest):
    try:
        await asyncio.sleep(0.01)
        response = SimpleResponse(status="success", data=request.data)
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
