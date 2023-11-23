import uvicorn
from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel
from typing import List, Tuple
from functions import *

app = FastAPI()

class RequestBody(BaseModel):
    month: int
    day: str
    time: str
    subwayStop: str
    direction: str

class ResponseBody(BaseModel):
    status: str
    data: List[Tuple[str, int]]

@app.get("/")
def printinfo():
    return "ANZIP API"

@app.post("/send")
async def your_api_function(request_body: RequestBody):
    value = maindef(month=request_body.month, day=request_body.day, time=request_body.time,
                    subwayStop=request_body.subwayStop, direction=request_body.direction)
    status = value[0]
    data = value[1]
    # ResponseBody 모델을 이용하여 응답 데이터를 반환
    response_model = ResponseBody(status=status, data=data)
    return response_model




# @app.get("/send")
# async def your_api_function(month: int, day: str, time: str, subwayStop: str, direction: str):
#     value = maindef(
#         month=month,
#         day=day,
#         time=time,
#         subwayStop=subwayStop,
#         direction=direction
#     )
#     status = value[0]
#     data = value[1]
#
#     response_model = ResponseBody(status=status, data=data)
#
#     return response_model

