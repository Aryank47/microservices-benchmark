import asyncio
import json
import time

from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse

router = APIRouter()


async def generate_stream_data(number_of_messages: int):
    for i in range(number_of_messages):
        yield json.dumps(
            {"data": f"Message {i}", "timestamp": int(time.time() * 1000)}
        ) + "\n"
        await asyncio.sleep(0.01)


@router.get("/stream")
async def stream_data(messages: int = 100):
    try:
        return StreamingResponse(
            generate_stream_data(messages), media_type="application/x-ndjson"
        )
    except Exception as e:

        raise HTTPException(status_code=500, detail=str(e))
