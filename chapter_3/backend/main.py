import asyncio
import json
from fastapi import FastAPI
from fastapi.responses import JSONResponse, StreamingResponse
from fastapi_profiler import Profiler
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()
Profiler(app)

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # frontend dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get('/')
async def root():
    return "Hello world!"


# --------- Polling APIs -------------------

global last_read_position

def read_commentary(count, memo={}):
    """Mimicing read for polling, one by one"""
    last_read_position = memo.get('last_read_position', 0)
    with open('commentary.json', 'r') as fh:
        data = json.load(fh)
        required_data = data[last_read_position: last_read_position+count]
    memo['last_read_position'] = last_read_position+count
    return required_data

@app.get('/polling/logs/{count}')
async def read_next_line(count: int):
    return read_commentary(count)


# ------- Server sent events ----------------

async def stream_commentary():
    # with open('commentary.json', 'r') as fh:
    #     data = json.load(fh)
    #     for row in data:
    #         yield row
    
    for i in range(100):
        await asyncio.sleep(1)
        yield str(i)


@app.get('/sse/logs')
async def stream_logs():
    return StreamingResponse(stream_commentary(), media_type='text/event-stream')