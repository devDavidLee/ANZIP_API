import uvicorn
from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel
from typing import List, Tuple
from functions import *

app = FastAPI()

class ResponseBody(BaseModel):
    status: str
    data: List[Tuple[str, int]]

@app.get("/")
def printinfo():
    return "ANZIP API"

@app.get("/send")
async def your_api_function(month: int, day: str, time: str, subwayStop: str, direction: str):
    value = maindef(
        month=month,
        day=day,
        time=time,
        subwayStop=subwayStop,
        direction=direction
    )
    status = value[0]
    data = value[1]

    response_model = ResponseBody(status=status, data=data)

    return response_model

