import uvicorn
from fastapi import FastAPI, Request
import requests

class TraceHeader:
    TRACE_ID = "x-trace-id"
    SOURCE_ID = "x-trace-source-id"
    PARENT_ID = "x-trace-parent-id"
    TIME = "x-trace-timestamp"
    IS_COMPLETE = "is_complete"


SERVICE_3_URL = "http://service-3/"
SERVICE_4_URL = "http://service-4/"


app = FastAPI()

            
def make_request(url, request_headers: dict):
    print(f"calling service at {url}")
    
    headers = {"Content-Type": "application/json"}
    headers[TraceHeader.TRACE_ID] = request_headers[TraceHeader.TRACE_ID]
    headers[TraceHeader.PARENT_ID] = request_headers[TraceHeader.PARENT_ID]
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        print(f"success hitting {url}")
    else:
        print(f"failed hitting {url}")


@app.get("/ping")
async def ping():
    return {"message": "pong"}


@app.get("/")
async def task(request: Request):
    make_request(SERVICE_3_URL, request.headers)
    make_request(SERVICE_4_URL, request.headers)
    return {"message": "Hello from Service-2"}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)