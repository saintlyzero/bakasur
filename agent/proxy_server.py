import logging
import os
import time
import uuid
from contextlib import asynccontextmanager
from typing import Optional, Tuple

import httpx
import uvicorn
from fastapi import FastAPI, Request
from fastapi.responses import StreamingResponse
from httpx import AsyncClient
from starlette.background import BackgroundTask
from starlette.datastructures import Headers

TRACE_SOURCE_ID = os.getenv("TRACE_SOURCE_ID", "local_service")
SERVICE_ENDPOINT = "http://127.0.0.1:8000/"
COLLECTOR_ENDPOINT = "http://collector/trace"
REQUEST_TIMEOUT = 10

timeout = httpx.Timeout(None)
class TraceHeader:
    TRACE_ID = "x-trace-id"
    SOURCE_ID = "x-trace-source-id"
    PARENT_ID = "x-trace-parent-id"
    TIME = "x-trace-timestamp"
    IS_COMPLETE = "is_complete"


class TraceLabel:
    TRACE_ID = "trace_id"
    SOURCE_ID = "source_id"
    PARENT_ID = "parent_id"
    TIME = "timestamp"
    IS_COMPLETE = "is_complete"


logging.basicConfig(level=logging.INFO)


class TraceData:
    def __init__(
        self,
        trace_id: str = "",
        source_id: str = "",
        parent_id: Optional[str] = None,
        is_complete: bool = False,
    ) -> None:
        self.trace_id = trace_id
        self.source_id = source_id
        self.parent_id = parent_id
        self.timestamp = int(time.time())
        self.is_complete = is_complete

    def get_dict(self) -> dict:
        return {
            TraceLabel.TRACE_ID: self.trace_id,
            TraceLabel.SOURCE_ID: self.source_id,
            TraceLabel.PARENT_ID: self.parent_id,
            TraceLabel.TIME: self.timestamp,
            TraceLabel.IS_COMPLETE: self.is_complete,
        }

    def set_complete(self):
        self.is_complete = True
        self.timestamp = int(time.time())


def process_headers(headers: Headers) -> Tuple[Headers, TraceData]:
    updated_headers = headers.mutablecopy()

    # fresh request in the system
    if TraceHeader.TRACE_ID not in updated_headers:
        updated_headers[TraceHeader.TRACE_ID] = uuid.uuid4().hex

    parent_id = updated_headers.get(TraceHeader.PARENT_ID)

    # make source as parent for future requests
    updated_headers[TraceHeader.PARENT_ID] = TRACE_SOURCE_ID

    trace_data = TraceData(
        trace_id=updated_headers[TraceHeader.TRACE_ID],
        source_id=TRACE_SOURCE_ID,
        parent_id=parent_id,
    )

    return updated_headers, trace_data


@asynccontextmanager
async def set_http_client(app: FastAPI):
    try:
        logging.info("creating AsyncClient client")
        client = AsyncClient(base_url=SERVICE_ENDPOINT, timeout=timeout)
        app.state.service_client = client
        yield
    except Exception as e:
        logging.error("Error creating AsyncClient")
        logging.error(e)
    finally:
        logging.info("closing AsyncClient client")
        await client.aclose()


async def hit_collector(trace_data: TraceData):
    async with httpx.AsyncClient() as client:
        headers = {"Content-Type": "application/json"}
        response = await client.post(
            COLLECTOR_ENDPOINT, headers=headers, json=trace_data.get_dict(),
            timeout=timeout
        )

        if response.status_code == 200:
            logging.info("success hitting trace collector")
        else:
            logging.error("failed hitting trace collector")


app = FastAPI(lifespan=set_http_client)


async def _reverse_proxy(request: Request):
    client = request.app.state.service_client
    url = httpx.URL(path=request.url.path, query=request.url.query.encode("utf-8"))
    updated_header, trace_data = process_headers(request.headers)
    await hit_collector(trace_data)

    rp_req = client.build_request(
        request.method, url, headers=updated_header.raw, content=await request.body()
    )

    print("Service Request: INIT")
    rp_resp = await client.send(rp_req, stream=True)
    print("Service Response: SUCCESS")

    trace_data.set_complete()
    await hit_collector(trace_data)

    return StreamingResponse(
        rp_resp.aiter_raw(),
        status_code=rp_resp.status_code,
        headers=rp_resp.headers,
        background=BackgroundTask(rp_resp.aclose),
    )


app.add_route("/{path:path}", _reverse_proxy, ["GET"])

if __name__ == "__main__":
    uvicorn.run("proxy_server:app", host="0.0.0.0", port=9000, reload=True)
