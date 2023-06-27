from typing import Optional
from pydantic import *


class Ingredient(BaseModel):
    id_bahan: int
    quantity: Optional[int] = None
    satuan: str

class RecipeSchema(BaseModel):
    name: str
    description: str
    id_kategori: int
    ingredients: conlist(Ingredient, min_items=1)

class RecipeUpdateSchema(BaseModel):
    id_recipe: int
    name: str
    description: str
    id_kategori: int
    ingredients: Optional[conlist(Ingredient, min_items=1)] = None

class RecipeDeleteSchema(BaseModel):
    id_recipe: int