from typing import Optional

from fastapi import FastAPI, Depends
from fastapi_health import health
#from model.model import Emprendedor

from pydantic import BaseModel

class Emprendedor(BaseModel):
    name:str

def get_session():
    return True

def is_database_online(session: bool = Depends(get_session)):
    return session

app = FastAPI()


@app.get("/")
def read_root():
    return {"Emprendedores"}

@app.get("/emprendedores/{emprendedor_id}")
def read_item(emprendedor_id: int, q: Optional[str] = None):
    return {"emprendedor_id": emprendedor_id, "q": q}

@app.put("/emprendedores/{emprendedor_id}")
def update_emprendedor(emprendedor_id: int, emprendedor: Emprendedor):
    return {"emprendedor_name": emprendedor.name, "emprendedor_id": emprendedor_id}


app.add_api_route("/health", health([is_database_online]))
