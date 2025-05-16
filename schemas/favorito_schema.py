from marshmallow import fields, post_load
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from modelos.favorito_model import Favorito
from schemas.simple.post_simple_schema import PostSimpleSchema


class FavoritoSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Favorito
        load_instance = True
        include_relationships = False
    
    id_usuario = fields.Str(required=True, load_only=True)  # UUID para deserialización en las solicitudes post y put)
    id_post    = fields.Str(required=True, load_only=True)     
    usuario    = fields.Nested("UserSchema", dump_only=True)  # Relación con Usuario
    post       = fields.Nested(PostSimpleSchema, dump_only=True)  # Relación con Post

    @post_load
    def make_favorito(self, data, **kwargs):
        # Crear instancia de Favorito asignando campos
        return Favorito(
            id_usuario=data['id_usuario'],
            id_post=data['id_post']
        )