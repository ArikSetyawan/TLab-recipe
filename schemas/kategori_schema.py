from typing import Optional
from pydantic import *

class KategoriCreateSchema(BaseModel):
    name: str

class KategoriUpdateSchema(BaseModel):
    id_kategori: int
    name: str

class KategoriDeleteSchema(BaseModel):
    id_kategori: int