from fastapi import FastAPI
from pydantic import BaseModel
from Backend.models import EPRequest, EPResponse  
from Backend.Orchestor import evaluar_ep

app = FastAPI()

@app.post("/eval_ep", response_model=EPResponse)
def evaluar_ep_endpoint(payload: EPRequest):
    result = evaluar_ep(payload)
    return result
