from marshmallow import fields, Schema
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from modelos.favorito_model import Favorito
from schemas.simple.post_simple_schema import PostSimpleSchema
from extensions import db
from schemas.user_schema import UserSchema


class FavoritoSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Favorito
        load_instance = True
        include_relationships = False
        sqla_session = db.session
        schema_name="FavoritoSchema"
    
    id_usuario = fields.Str(required=True, load_only=True)  
    id_post    = fields.Str(required=True, load_only=True)     
    usuario    = fields.Nested(UserSchema, only=("id_usuario", "nombre", "email"), dump_only=True)      # Relación con Usuario
    post       = fields.Nested(PostSimpleSchema, dump_only=True)  # Relación con Post


class FavoritoInputSchema(Schema):
    id_post = fields.Str(required=True)

class FavoritoResponseSchema(Schema):
    mensaje = fields.String()
    id_usuario = fields.String()
    id_post = fields.String()