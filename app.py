from flask import Flask, request
from flask_restx import Api, Resource, reqparse
from peewee import *
from playhouse.shortcuts import model_to_dict
from pydantic import ValidationError

# Import Schema

from schemas.recipe_schema import RecipeSchema, RecipeUpdateSchema, RecipeDeleteSchema
from schemas.bahan_schema import BahanCreateSchema, BahanUpdateSchema, BahanDeleteSchema
from schemas.kategori_schema import KategoriCreateSchema, KategoriUpdateSchema, KategoriDeleteSchema

import dotenv, os


dotenv.load_dotenv()

# SQLITE
# db = 'mydatabase.db'
# database = SqliteDatabase(db)

# MySQL PRODUCTION
# database = MySQLDatabase(os.getenv('DATABASE_NAME'), user=os.getenv('DATABASE_PROD_USER'), password=os.getenv('DATABASE_PROD_PASSWORD'), host=os.getenv('DATABASE_PROD_HOST'), port=int(os.getenv('DATABASE_PROD_PORT')))

# MySQL DEV
database = MySQLDatabase(os.getenv('DATABASE_NAME'), user=os.getenv('DATABASE_DEV_USER'), host=os.getenv('DATABASE_DEV_HOST'), port=int(os.getenv('DATABASE_DEV_PORT')))

class BaseModel(Model):
    class Meta:
        database = database

class Bahan(BaseModel):
    id = AutoField()
    name = CharField(unique=True)

class Kategori(BaseModel):
    id = AutoField()
    name = CharField(unique=True)

class Recipe(BaseModel):
    id = AutoField()
    name = CharField()
    description = TextField()
    kategori = ForeignKeyField(Kategori, backref='recipes', column_name = 'id_kategori')

class RecipeBahan(BaseModel):
    id = AutoField()
    recipe = ForeignKeyField(Recipe, backref='recipe_bahan', column_name = 'id_recipe')
    bahan = ForeignKeyField(Bahan, backref='recipe_bahan', column_name = 'id_bahan')
    quantity = IntegerField(null=True)
    satuan = CharField()

def create_tables():
    with database:
        database.create_tables([Bahan, Kategori, Recipe, RecipeBahan])


app = Flask(__name__)
api = Api(app)


class ResponseSchema():
    def ResponseJson(success: bool = True, message: str = None, data: dict|list = None, error : dict|list = None):
        return {
            'success': success,
            'message': message,
            'data': data,
            'error': error
        }

class ResourceBahan(Resource):
    def get(self):
        # define the arguments to accept
        parser = reqparse.RequestParser()
        parser.add_argument('id_bahan', type=int, location='args')
        args = parser.parse_args()
        # if id_bahan in arguments, it will try to return Bahan with given id
        if args['id_bahan'] is not None:
            # Get bahan with this id_bahan
            bahan = Bahan.select().where(Bahan.id == args['id_bahan'])
            # Check if bahan is exists. if bahan exists. it will return single record of bahan with given id
            if not bahan.exists():
                return ResponseSchema.ResponseJson(success=False, message='Bahan Not Found', data=None),404
            bahan = bahan.dicts().get()
            return ResponseSchema.ResponseJson(success=True, message='Bahan Found', data=bahan),200
        
        # Get all bahan
        bahan = list(Bahan.select().dicts())
        return ResponseSchema.ResponseJson(success=True, message='Bahan Found', data=bahan),200
    
    def post(self):
        # define the required data to accept
        try:
            bahan = BahanCreateSchema(**request.json)
        except ValidationError as e:
            return ResponseSchema.ResponseJson(success=False, message='Bahan Not Created', data=None, error={"message":e.errors()}),400
        # Create new bahan
        try:
            newBahan = Bahan.create(name=bahan.name)
            return ResponseSchema.ResponseJson(success=True, message='Bahan Created', data=model_to_dict(newBahan)),201
        except Exception as e:
            return ResponseSchema.ResponseJson(success=False, message='Bahan Not Created', data=None, error={"message":str(e)}),400
        
    def put(self):
        # define the required data to accept
        try:
            bahan = BahanUpdateSchema(**request.json)
        except ValidationError as e:
            return ResponseSchema.ResponseJson(success=False, message='Bahan Not Updated', data=None, error={"message":e.errors()}),400
        
        # Check bahan with given id_bahan exists
        getBahan = Bahan.select().where(Bahan.id == bahan.id_bahan)
        if not getBahan.exists():
            return ResponseSchema.ResponseJson(success=False, message='Bahan Not Found', data=None),404
        
        # Update bahan with given id_bahan
        try:
            Bahan.update(name=bahan.name).where(Bahan.id == bahan.id_bahan).execute()
            getBahan = Bahan.get(id = bahan.id_bahan)
            return ResponseSchema.ResponseJson(success=True, message='Bahan Updated', data=model_to_dict(getBahan)),200
        except Exception as e:
            return ResponseSchema.ResponseJson(success=False, message='Bahan Not Updated', data=None, error={"message":str(e)}),400
        
    def delete(self):
        # define the required data to accept
        try:
            bahan = BahanDeleteSchema(**request.json)
        except ValidationError as e:
            return ResponseSchema.ResponseJson(success=False, message='Bahan Not Deleted', data=None, error={"message":e.errors()}),400
        
        # Check bahan with given id_bahan exists
        getBahan = Bahan.select().where(Bahan.id == bahan.id_bahan)
        if not getBahan.exists():
            return ResponseSchema.ResponseJson(success=False, message='Bahan Not Found', data=None),404
        
        # Check if bahan is used in recipe
        recipe_bahan = RecipeBahan.select().where(RecipeBahan.id_bahan == bahan.id_bahan)
        if recipe_bahan.exists():
            return ResponseSchema.ResponseJson(success=False, message='Bahan Used In Recipe', data=None),400

        # Delete bahan with given id_bahan
        try:
            Bahan.delete().where(Bahan.id == bahan.id_bahan).execute()
            return ResponseSchema.ResponseJson(success=True, message='Bahan Deleted', data=None),200
        except Exception as e:
            return ResponseSchema.ResponseJson(success=False, message='Bahan Not Deleted', data=None, error={"message":str(e)}),400

class ResourceKategori(Resource):
    def get(self):
        # define the arguments to accept
        parser = reqparse.RequestParser()
        parser.add_argument('id_kategori', type=int, location='args')
        args = parser.parse_args()
        # if id_kategori in arguments, it will try to return Kategori with given id
        if args['id_kategori'] is not None:
            # Get kategori with this id_kategori
            kategori = Kategori.select().where(Kategori.id == args['id_kategori'])
            # Check if kategori is exists. if kategori exists. it will return single record of kategori with given id
            if not kategori.exists():
                return ResponseSchema.ResponseJson(success=False, message='Kategori Not Found', data=None),404
            kategori = kategori.dicts().get()
            return ResponseSchema.ResponseJson(success=True, message='Kategori Found', data=kategori),200
        
        # Get all kategori
        kategori = list(Kategori.select().dicts())
        return ResponseSchema.ResponseJson(success=True, message='Kategori Found', data=kategori),200
    
    def post(self):
        # define the required data to accept
        try:
            kategori = KategoriCreateSchema(**request.json)
        except ValidationError as e:
            return ResponseSchema.ResponseJson(success=False, message='Kategori Not Created', data=None, error=e.errors()),400

        # Create new kategori
        try:
            newKategori = Kategori.create(name=kategori.name)
            return ResponseSchema.ResponseJson(success=True, message='Kategori Created', data=model_to_dict(newKategori)),201
        except Exception as e:
            return ResponseSchema.ResponseJson(success=False, message='Kategori Not Created', data=None, error={"message":str(e)}),400
        
    def put(self):
        # define the required data to accept
        try:
            kategori = KategoriUpdateSchema(**request.json)
        except ValidationError as e:
            return ResponseSchema.ResponseJson(success=False, message='Kategori Not Updated', data=None, error=e.errors()),400
        
        # Check kategori with given id_kategori exists
        getKategori = Kategori.select().where(Kategori.id == kategori.id_kategori)
        if not getKategori.exists():
            return ResponseSchema.ResponseJson(success=False, message='Kategori Not Found', data=None),404
        
        # Update kategori with given id_kategori
        try:
            Kategori.update(name=kategori.name).where(Kategori.id == kategori.id_kategori).execute()
            getKategori = Kategori.get(id = kategori.id_kategori)
            return ResponseSchema.ResponseJson(success=True, message='Kategori Updated', data=model_to_dict(getKategori)),200
        except Exception as e:
            return ResponseSchema.ResponseJson(success=False, message='Kategori Not Updated', data=None, error={"message":str(e)}),400
        
    def delete(self):
        # define the required data to accept
        try:
            kategori = KategoriDeleteSchema(**request.json)
        except ValidationError as e:
            return ResponseSchema.ResponseJson(success=False, message='Kategori Not Deleted', data=None, error=e.errors()),400
        
        # Check kategori with given id_kategori exists
        getKategori = Kategori.select().where(Kategori.id == kategori.id_kategori)
        if not getKategori.exists():
            return ResponseSchema.ResponseJson(success=False, message='Kategori Not Found', data=None),404
        
        # Check if kategori is used in recipe
        recipe_kategori = Recipe.select().where(Recipe.id_kategori == kategori.id_kategori)
        if recipe_kategori.exists():
            return ResponseSchema.ResponseJson(success=False, message='Kategori Used In Recipe', data=None),400
        
        # Delete kategori with given id_kategori
        try:
            Kategori.delete().where(Kategori.id == kategori.id_kategori).execute()
            return ResponseSchema.ResponseJson(success=True, message='Kategori Deleted', data=None),200
        except Exception as e:
            return ResponseSchema.ResponseJson(success=False, message='Kategori Not Deleted', data=None, error={"message":str(e)}),400
        
class ResourceRecipe(Resource):
    def get(self):
        # define the arguments to accept
        parser = reqparse.RequestParser()
        parser.add_argument('id_recipe', type=int, location='args')
        parser.add_argument('id_kategori', type=int, location='args')
        parser.add_argument('id_bahan', type=int, location='args')
        args = parser.parse_args()


        # if id_recipe in arguments, it will try to return Recipe with given id
        if args['id_recipe'] is not None:
            # Get recipe with this id_recipe
            recipe = Recipe.select().join(RecipeBahan).join(Bahan).where(Recipe.id == args['id_recipe'])
            # Check if recipe is exists. if recipe exists. it will return single record of recipe with given id
            if not recipe.exists():
                return ResponseSchema.ResponseJson(success=False, message='Recipe Not Found', data=None),404
            recipe = model_to_dict(recipe.get(), backrefs=True)
            return ResponseSchema.ResponseJson(success=True, message='Recipe Found', data=recipe),200
        
        # if id_kategori and id_bahan in arguments, it will try to return Recipe with given id_kategori and id_bahan
        if args['id_kategori'] is not None and args['id_bahan'] is not None:
            # Get recipe with given id_kategori and id_bahan
            recipe = Recipe.select().join(RecipeBahan).join(Bahan).where(Recipe.id_kategori == args['id_kategori'], RecipeBahan.id_bahan == args['id_bahan'])
            recipe = [model_to_dict(r, backrefs=True) for r in recipe]
            return ResponseSchema.ResponseJson(success=True, message='Recipe Found', data=recipe),200
        
        # if id_kategori in arguments, it will try to return Recipe with given id_kategori
        if args['id_kategori'] is not None:
            # check if kategori exists
            kategori = Kategori.select().where(Kategori.id == args['id_kategori'])
            if not kategori.exists():
                return ResponseSchema.ResponseJson(success=False, message='Kategori Not Found', data=None),404
            recipe = Recipe.select().where(Recipe.id_kategori == args['id_kategori'])
            # Check if recipe is exists. if recipe exists. it will return single record of recipe with given id
            recipe = [model_to_dict(r, backrefs=True) for r in recipe]
            return ResponseSchema.ResponseJson(success=True, message='Recipe Found', data=recipe),200
        
        # if id_bahan in arguments, it will try to return Recipe with given id_bahan
        if args['id_bahan'] is not None:
            # check if bahan exists
            bahan = Bahan.select().where(Bahan.id == args['id_bahan'])
            if not bahan.exists():
                return ResponseSchema.ResponseJson(success=False, message='Bahan Not Found', data=None),404
            
            recipe = Recipe.select().join(RecipeBahan).join(Bahan).where(RecipeBahan.id_bahan == args['id_bahan'])
            # Check if recipe is exists. if recipe exists. it will return single record of recipe with given id
            recipes = [model_to_dict(r, backrefs=True) for r in recipe]
            return ResponseSchema.ResponseJson(success=True, message='Recipe Found', data=recipes),200

        # Get all recipe
        recipe = [model_to_dict(r, backrefs=True) for r in Recipe.select().join(RecipeBahan).join(Bahan)]
        return ResponseSchema.ResponseJson(success=True, message='Recipe Found', data=recipe),200
    
    def post(self):
        try:
            # parse args to Recipe Schema
            recipe = RecipeSchema(**request.json)
        except ValidationError as e:
            return ResponseSchema.ResponseJson(success=False, message='Recipe Not Created', data=None, error=e.errors()),400
        
        # Check if id_kategori exists
        kategori = Kategori.select().where(Kategori.id == recipe.id_kategori)
        if not kategori.exists():
            return ResponseSchema.ResponseJson(success=False, message='Kategori Not Found', data=None),404
        
        # loop recipe ingredients and check if bahan exists
        for bahan in recipe.ingredients:
            bahan = Bahan.select().where(Bahan.id == bahan.id_bahan)
            if not bahan.exists():
                return ResponseSchema.ResponseJson(success=False, message='Bahan Not Found', data=None),404
        
        # Create new recipe
        newRecipe = Recipe.create(name=recipe.name, description=recipe.description, kategori=recipe.id_kategori)
        for bahan in recipe.ingredients:
            RecipeBahan.create(recipe=newRecipe.id, bahan=bahan.id_bahan, quantity=bahan.quantity, satuan=bahan.satuan)


        # Getting the newly created recipe
        recipe = model_to_dict(newRecipe, backrefs=True)
        return ResponseSchema.ResponseJson(success=True, message='Recipe Created', data=recipe),201
    
    def put(self):
        try:
            recipe = RecipeUpdateSchema(**request.json)
            # return ResponseSchema.ResponseJson(success=True, message='Recipe Updated', data=recipe.dict()),200
        except ValidationError as e:
            return ResponseSchema.ResponseJson(success=False, message='Recipe Not Updated', data=None, error=e.errors()),400
        
        # try to get recipe with given id_recipe
        getRecipe = Recipe.select().where(Recipe.id == recipe.id_recipe)
        if not getRecipe.exists():
            return ResponseSchema.ResponseJson(success=False, message='Recipe Not Found', data=None),404
        getRecipe = getRecipe.get()

        # check if id_kategori in recipe is exists
        getKategori = Kategori.select().where(Kategori.id == recipe.id_kategori)
        if not getKategori.exists():
            return ResponseSchema.ResponseJson(success=False, message='Kategori Not Found', data=None),404
        
        # Check Ingredients in recipe is Not Null
        if recipe.ingredients is not None:
            for bahan in recipe.ingredients:
                bahan = Bahan.select().where(Bahan.id == bahan.id_bahan)
                if not bahan.exists():
                    return ResponseSchema.ResponseJson(success=False, message='Bahan Not Found', data=None),404

        
        # Update recipe with given id_recipe
        getRecipe.update(name=recipe.name, description=recipe.description, kategori=recipe.id_kategori).execute()

        if recipe.ingredients is not None:
            # delete RecipeBahan with given id_recipe
            RecipeBahan.delete().where(RecipeBahan.recipe == getRecipe.id).execute()

            # loop recipe ingredients and create RecipeBahan
            for bahan in recipe.ingredients:
                RecipeBahan.create(recipe=recipe.id_recipe, bahan=bahan.id_bahan, quantity=bahan.quantity, satuan=bahan.satuan)

        # Get updated recipe
        recipe = model_to_dict(Recipe.get(id=recipe.id_recipe), backrefs=True)

        return ResponseSchema.ResponseJson(success=True, message='Recipe Updated', data=recipe),200
    
    def delete(self):
        try:
            recipe = RecipeDeleteSchema(**request.json)
        except ValidationError as e:
            return ResponseSchema.ResponseJson(success=False, message='Recipe Not Deleted', data=None, error=e.errors()),400
        
        # Check recipe with given id_recipe exists
        getRecipe = Recipe.select().where(Recipe.id == recipe.id_recipe)
        if not getRecipe.exists():
            return ResponseSchema.ResponseJson(success=False, message='Recipe Not Found', data=None),404
        
        # Delete recipe and recipebahan with given id_recipe
        RecipeBahan.delete().where(RecipeBahan.recipe == recipe.id_recipe).execute()
        Recipe.delete().where(Recipe.id == recipe.id_recipe).execute()
        return ResponseSchema.ResponseJson(success=True, message='Recipe Deleted', data=None),200
        


api.add_resource(ResourceBahan, '/api/bahan')
api.add_resource(ResourceKategori, '/api/kategori')
api.add_resource(ResourceRecipe, '/api/recipe')

if __name__ == '__main__':
    create_tables()
    app.run(debug=True)