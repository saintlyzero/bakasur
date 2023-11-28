import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from tortoise.contrib.fastapi import register_tortoise
from models import Trace
from tortoise import Tortoise
from graph import Graph

DUMMY_GRAPH = {
            'name': 'service-1',
            'isComplete': 1,
            'processingTime': 8,
            'children': [{
                'name': 'service-2',
                'isComplete': 1,
                'processingTime': 4,
                'children': [{
                    'name': 'service-3',
                    'isComplete': 1,
                    'processingTime': 2,
                    'children': []
                }, {
                    'name': 'service-4',
                    'isComplete': 1,
                    'processingTime': 2,
                    'children': []
                }]
            }, {
                'name': 'service-5',
                'isComplete': 1,
                'processingTime': 1,
                'children': [{
                    'name': 'service-6',
                    'isComplete': 1,
                    'processingTime': 1,
                    'children': []
                }]
            }, {
                'name': 'service-7',
                'isComplete': 1,
                'processingTime': 3,
                'children': []
            }]
        }

DYMMY_TRACES = [
  {
    "trace_id": "61d97881fe7d4048950e1f6b61ae518e",
    "processing_time": "8s"
  },
  {
    "trace_id": "31bbbf9defb34a25af0829964102818b",
    "processing_time": "10s"
  },
  {
    "trace_id": "569455fd821b4993bff81f68ca5b6e2d",
    "processing_time": "12s"
  },
  {
    "trace_id": "40e7e7b4d37e422f9036de94a43f9c49",
    "processing_time": "7s"
  },
  {
    "trace_id": "aceedff31bd444cab0294c8da25fa2ec",
    "processing_time": "9s"
  }
]

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
async def graph(traceId:str):
  db_traces = await Trace.filter(trace_id=traceId)
  
  traces = [record.to_dict() for record in db_traces]

  graph = Graph(traceId)
  return graph.get_tree_graph(traces)

@app.get("/trace")
async def list_traces():
  db_connection = Tortoise.get_connection("default")
  query = """
    SELECT trace_id,
        NULLIF(out_time, NULL) - NULLIF(in_time, NULL) AS 'Processing Time',
        FROM_UNIXTIME(in_time) AS 'In Time'
    FROM   trace
    WHERE  from_node IS NULL
    ORDER BY in_time DESC; 
  """
  return await db_connection.execute_query_dict(query)

if __name__ == "__main__":
    print("v-backend running on 9000")
    uvicorn.run("main:app", host="0.0.0.0", port=9000, reload=True)
    
