import asyncio
import datetime
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
# Documentation for SSE: 
# https://developer.mozilla.org/en-US/docs/Web/API/Server-sent_events/Using_server-sent_events


class SSEModel:
    def __init__(self, data, _id=None, event=None) -> None:
        self.data = data
        self.id = datetime.datetime.now() if _id is None else _id
        self.event = event      # Allows us to use named events at client side. 
    
    def __str__(self):
        if self.event is None:
            return f'id: {self.id}\ndata: {self.data}\n\n'
        else:    
            return f'id: {self.id}\nevent: {self.event}\ndata: {self.data}\n\n'

async def stream_commentary(mode):
    if mode == 'commentary':
    # Example with commentary data
        with open('commentary.json', 'r') as fh:
            data = json.load(fh)
            for row in data:
                await asyncio.sleep(1)
                yield str(SSEModel(row, event="Digit"))
        
        yield str(SSEModel(None, event="Completed"))
    
    elif mode == 'simple':
    # Simpler example. Returns number
        for i in range(100):
            await asyncio.sleep(1)
            yield str(SSEModel(i))
        
        yield str(SSEModel(None, event="Completed"))
    
    else:
        yield str(SSEModel(f'{mode} is not a valid mode', event="error"))

@app.get('/sse/logs/{mode}')
async def stream_logs(mode:str):
    headers = {'Content-Type': 'text/event-stream', 
                                      'Connection': 'keep-alive', 
                                      "Cache-Control": "no-cache"}
    return StreamingResponse(stream_commentary(mode), 
                             media_type="text/event-stream",
                             headers=headers)
