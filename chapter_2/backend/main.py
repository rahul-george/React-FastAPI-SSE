import json
from fastapi import FastAPI
from fastapi_profiler import Profiler


app = FastAPI()
Profiler(app)

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