from pydantic import BaseModel

class ResponseMessage(BaseModel):
    status: int
    results: dict
