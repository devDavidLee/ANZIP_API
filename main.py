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

class commentsBody(BaseModel):
    score: int
    comment: str

class ResponseBody(BaseModel):
    status: str
    data: List[Tuple[str, int]]

@app.get("/")
def printinfo():
    return "ANZIP API"

@app.post("/send")
async def senddata(request_body: RequestBody):
    value = maindef(month=request_body.month, day=request_body.day, time=request_body.time,
                    subwayStop=request_body.subwayStop, direction=request_body.direction)
    status = value[0]
    d = value[1]
    data = list()
    for i in range(len(d)):
        data.append(list(d[i]))
    # ResponseBody 모델을 이용하여 응답 데이터를 반환
    response_model = ResponseBody(status=status, data=data)
    return response_model

@app.post("/comments")
async def getcomments(comments_body: commentsBody):
    satis = comments_body.score
    comments = comments_body.comment
    return {satis: comments}


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
