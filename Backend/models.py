from pydantic import BaseModel
from typing import List, Dict

class EPRequest(BaseModel):
    ficha_medica: Dict
    ficha_psicologica: Dict
    ept: Dict
    output_fm: str
    output_fp: str
    output_ept: str

class EPResponse(BaseModel):
    respuesta_final: str
    razonamiento: List[str]
