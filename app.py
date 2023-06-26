from flask import Flask, jsonify
from flask_restx import Api, Resource, reqparse
from peewee import *
from playhouse.shortcuts import model_to_dict

db = 'mydatabase.db'
database = SqliteDatabase(db)

class BaseModel(Model):
    class Meta:
        database = database

class Bahan(BaseModel):
    id = AutoField()
    name = CharField(unique=True)

class Kategori(BaseModel):
    id = AutoField()
    name = CharField()

class Recipe(BaseModel):
    id = AutoField()
    name = CharField()
    description = TextField()
    id_kategori = ForeignKeyField(Kategori, backref='recipes')

class RecipeBahan(BaseModel):
    id = AutoField()
    id_recipe = ForeignKeyField(Recipe, backref='recipe_bahan')
    id_bahan = ForeignKeyField(Bahan, backref='recipe_bahan')
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
        parser = reqparse.RequestParser()
        parser.add_argument('name', type=str, required=True, location='json')
        args = parser.parse_args()
        # Create new bahan
        try:
            bahan = Bahan.create(name=args['name'])
            return ResponseSchema.ResponseJson(success=True, message='Bahan Created', data=model_to_dict(bahan)),201
        except Exception as e:
            return ResponseSchema.ResponseJson(success=False, message='Bahan Not Created', data=None, error={"message":str(e)}),400
        
    def put(self):
        # define the required data to accept
        parser = reqparse.RequestParser(bundle_errors=True)
        parser.add_argument('id_bahan', type=int, required=True, location='json')
        parser.add_argument('name', type=str, required=True, location='json')
        args = parser.parse_args()
        
        # Check bahan with given id_bahan exists
        bahan = Bahan.select().where(Bahan.id == args['id_bahan'])
        if not bahan.exists():
            return ResponseSchema.ResponseJson(success=False, message='Bahan Not Found', data=None),404
        
        # Update bahan with given id_bahan
        try:
            Bahan.update(name=args['name']).where(Bahan.id == args['id_bahan']).execute()
            bahan = Bahan.get(id = args['id_bahan'])
            return ResponseSchema.ResponseJson(success=True, message='Bahan Updated', data=model_to_dict(bahan)),200
        except Exception as e:
            return ResponseSchema.ResponseJson(success=False, message='Bahan Not Updated', data=None, error={"message":str(e)}),400
        
    def delete(self):
        # define the required data to accept
        parser = reqparse.RequestParser()
        parser.add_argument('id_bahan', type=int, required=True, location='json')
        args = parser.parse_args()
        
        # Check bahan with given id_bahan exists
        bahan = Bahan.select().where(Bahan.id == args['id_bahan'])
        if not bahan.exists():
            return ResponseSchema.ResponseJson(success=False, message='Bahan Not Found', data=None),404
        
        # Check if bahan is used in recipe
        recipe_bahan = RecipeBahan.select().where(RecipeBahan.id_bahan == args['id_bahan'])
        if recipe_bahan.exists():
            return ResponseSchema.ResponseJson(success=False, message='Bahan Used In Recipe', data=None),400

        # Delete bahan with given id_bahan
        try:
            Bahan.delete().where(Bahan.id == args['id_bahan']).execute()
            return ResponseSchema.ResponseJson(success=True, message='Bahan Deleted', data=None),200
        except Exception as e:
            return ResponseSchema.ResponseJson(success=False, message='Bahan Not Deleted', data=None, error={"message":str(e)}),400

api.add_resource(ResourceBahan, '/api/bahan')

if __name__ == '__main__':
    create_tables()
    app.run(debug=True)