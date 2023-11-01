import logging

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from tortoise.contrib.fastapi import register_tortoise

from models import Trace
from pydantic import BaseModel

logging.basicConfig(level=logging.INFO)

class TraceLabel:
    TRACE_ID = "trace_id"
    SOURCE_ID = "trace_source_id"
    PARENT_ID = "trace_parent_id"
    TIME = "trace_timestamp"
    IS_COMPLETE = "is_complete"

app = FastAPI(title="Trace Collector")


register_tortoise(
    app,
    db_url="mysql://root:root@localhost:3306/bakasur",
    # db_url="mysql://root:root@mysql-service:3306/bakasur",
    modules={"models": ["models"]},
    generate_schemas=True,
    add_exception_handlers=True,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/ping")
async def root():
    return {"message": "pong"}

class TraceIn(BaseModel):
    trace_id: str
    source_id: str
    parent_id: str = None
    timestamp: int
    is_complete: bool = False

@app.post("/trace")
async def add_trace(trace_in:TraceIn):
    if trace_in.is_complete:
        trace = await Trace.get_or_none(
            trace_id =trace_in.trace_id,
            from_node=trace_in.parent_id, 
            to_node=trace_in.source_id)
        if not trace:
            logging.error("Trace does not exist")
            # todo: raise exception
            return
        trace.out_time = trace_in.timestamp 
        trace.is_complete = True
        await trace.save()
        
    else:
        trace = await Trace.create(
            trace_id =trace_in.trace_id,
            from_node=trace_in.parent_id, 
            to_node=trace_in.source_id, 
            in_time=trace_in.timestamp,
        )
    return {"trace": trace}


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=9001, reload=True)
