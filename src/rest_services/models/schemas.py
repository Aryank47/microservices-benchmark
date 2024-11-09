from typing import Dict

from pydantic import BaseModel


class SimpleRequest(BaseModel):
    message: str
    data: Dict[str, str]


class SimpleResponse(BaseModel):
    status: str
    data: Dict[str, str]


class PayloadRequest(BaseModel):
    data: bytes
    size_kb: int


class PayloadResponse(BaseModel):
    success: bool
    processed_size_kb: int
