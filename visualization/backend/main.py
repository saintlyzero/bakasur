import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from tortoise import Tortoise
from tortoise.contrib.fastapi import register_tortoise

from graph import Graph
from models import Trace

app = FastAPI(title="Visualization")

register_tortoise(
    app,
    # db_url="mysql://root:root@localhost:3306/bakasur",
    db_url="mysql://root:root@mysql-service:3306/bakasur",
    modules={"models": ["models"]},
    generate_schemas=False,
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
async def ping():
    return {"message": "pong"}


@app.get("/graph")
async def graph(traceId: str):
    db_traces = await Trace.filter(trace_id=traceId)

    traces = [record.to_dict() for record in db_traces]

    graph = Graph(traceId)
    return graph.get_tree_graph(traces)


@app.get("/trace")
async def list_traces():
    db_connection = Tortoise.get_connection("default")
    query = """
    SELECT trace_id,
        NULLIF(out_time, NULL) - NULLIF(in_time, NULL) AS 'Processing Time (s)',
        FROM_UNIXTIME(in_time) AS 'In Time'
    FROM   trace
    WHERE  from_node IS NULL
    ORDER BY in_time DESC; 
  """
    return await db_connection.execute_query_dict(query)


if __name__ == "__main__":
    print("v-backend running on 9000")
    uvicorn.run("main:app", host="0.0.0.0", port=9000, reload=True)
