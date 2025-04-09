from fastapi import FastAPI
from pydantic import BaseModel
from Orchestor import evaluar_ep
from models import EPRequest, EPResponse

app = FastAPI()

@app.post("/eval_ep", response_model=EPResponse)
def evaluar_ep_endpoint(payload: EPRequest):
    result = evaluar_ep(payload)
    return result
