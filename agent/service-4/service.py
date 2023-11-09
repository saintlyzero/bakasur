import random
import time

import uvicorn
from fastapi import FastAPI

app = FastAPI()


@app.get("/ping")
async def ping():
    return {"message": "pong"}


@app.get("/")
async def task():
    time.sleep(random.randint(1, 2))
    return {"message": "Hello from service-4"}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
