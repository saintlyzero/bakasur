import uvicorn
from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def ping():
    return {"message": "Hello from Service :)"}


@app.get("/test")
def test():
    return {"message": "TEST TEST"}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
