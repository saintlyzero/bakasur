import httpx
import uvicorn
from fastapi import FastAPI, Request
from fastapi.responses import StreamingResponse
from httpx import AsyncClient
from starlette.background import BackgroundTask
from fastapi import BackgroundTasks
from contextlib import asynccontextmanager
import logging

SERVICE_ENDPOINT = "http://127.0.0.1:8000/"
logging.basicConfig(level=logging.INFO)


@asynccontextmanager
async def set_http_client(app: FastAPI):
    try:
        logging.info("creating AsyncClient client")
        client = AsyncClient(base_url=SERVICE_ENDPOINT)
        app.state.client = client
        yield
    except Exception as e:
        logging.error("Error creating AsyncClient")
        logging.error(e)
    finally:
        logging.info("closing AsyncClient client")
        await client.aclose()


app = FastAPI(lifespan=set_http_client)


async def _reverse_proxy(request: Request):
    client = request.app.state.client
    url = httpx.URL(path=request.url.path, query=request.url.query.encode("utf-8"))
    rp_req = client.build_request(
        request.method, url, headers=request.headers.raw, content=await request.body()
    )
    rp_resp = await client.send(rp_req, stream=True)
    return StreamingResponse(
        rp_resp.aiter_raw(),
        status_code=rp_resp.status_code,
        headers=rp_resp.headers,
        background=BackgroundTask(rp_resp.aclose),
    )


app.add_route("/{path:path}", _reverse_proxy, ["GET"])

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=9000)
