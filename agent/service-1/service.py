import httpx
import uvicorn
from fastapi import FastAPI, Request


class TraceHeader:
    TRACE_ID = "x-trace-id"
    SOURCE_ID = "x-trace-source-id"
    PARENT_ID = "x-trace-parent-id"
    TIME = "x-trace-timestamp"
    IS_COMPLETE = "is_complete"


SERVICE_2_URL = "http://service-2/"
SERVICE_5_URL = "http://service-5/"
SERVICE_7_URL = "http://service-7/"

REQUEST_TIMEOUT = 120

app = FastAPI()
timeout = httpx.Timeout(10.0, read=None)


async def make_request(url, request_headers: dict):
    print(f"calling service at {url}")
    async with httpx.AsyncClient() as client:
        headers = {"Content-Type": "application/json"}
        headers[TraceHeader.TRACE_ID] = request_headers[TraceHeader.TRACE_ID]
        headers[TraceHeader.PARENT_ID] = request_headers[TraceHeader.PARENT_ID]

        response = await client.get(url, headers=headers, timeout=timeout)

        if response.status_code == 200:
            print(f"success hitting {url}")
        else:
            print(f"failed hitting {url}")


@app.get("/ping")
async def ping():
    return {"message": "pong"}


@app.get("/")
async def task(request: Request):
    await make_request(SERVICE_2_URL, request.headers)
    await make_request(SERVICE_5_URL, request.headers)
    await make_request(SERVICE_7_URL, request.headers)
    return {"message": "Hello from Service-1"}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
