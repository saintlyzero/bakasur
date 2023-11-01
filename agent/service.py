import time

import uvicorn
from fastapi import FastAPI, Request

app = FastAPI()


@app.get("/")
def ping(request: Request):
    print("microservice: IN")
    time.sleep(5)
    print("microservice: OUT")
    return {"message": "Hello from Service :)"}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
