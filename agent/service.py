import uvicorn
from fastapi import FastAPI, Request

app = FastAPI()


@app.get("/")
def ping(request: Request):
    print(f"x-trace-id: {request.headers.get('x-trace-id')}")
    print(f"x-trace-source-id: {request.headers.get('x-trace-id')}")
    return {"message": "Hello from Service :)"}


@app.get("/test")
def test():
    return {"message": "TEST TEST"}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
