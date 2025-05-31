from marshmallow import fields, Schema
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from modelos.favorito_model import Favorito
from schemas.simple.post_simple_schema import PostSimpleSchema
from extensions import db

class FavoritoSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Favorito
        load_instance = True
        include_relationships = False
        sqla_session = db.session
        schema_name="FavoritoSimpleSchema"
    
    id_usuario = fields.Str(required=True, load_only=True)  
    id_post    = fields.Str(required=True, load_only=True)     
    usuario    = fields.Nested("UserSchema", dump_only=True)      # Relación con Usuario
    post       = fields.Nested(PostSimpleSchema, dump_only=True)  # Relación con Post


class FavoritoInputSchema(Schema):
     model = Favorito
     load_instance = True
     include_relationships = False
     slqla_session = db.session
     schema_name = "FavoritoInputSchema"
     
     id_post = fields.Str(required=True, load_only=True)

class FavoritoResponseSchema(Schema):
    class Meta:
        model = Favorito
        load_instance = True
        include_relationships = False
        slqla_session = db.session
        schema_name = "FavoritoResponseSchema"

    mensaje = fields.String()
    id_usuario = fields.String()
    id_post = fields.String()