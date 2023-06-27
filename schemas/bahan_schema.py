from typing import Optional
from pydantic import *

class BahanCreateSchema(BaseModel):
    name:str

class BahanUpdateSchema(BaseModel):
    id_bahan:int
    name:str

class BahanDeleteSchema(BaseModel):
    id_bahan:int