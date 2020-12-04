from fastapi import FastAPI

from .api.endpoints import router as todo_router
from .database.utils import connect_mongo, disconnect_mongo


app = FastAPI(title="Todos API")

app.add_event_handler("startup", connect_mongo)
app.add_event_handler("shutdown", disconnect_mongo)

app.include_router(todo_router, prefix="/todos")


@app.get("/")
def index():
    return {"Hola": "Mundo"}
