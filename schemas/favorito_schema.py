from marshmallow import fields, post_load
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from modelos.favorito_model import Favorito


class FavoritoSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Favorito
        load_instance = True
        include_relationships = True
    
    id_usuario = fields.Str(required=True, load_only=True)  # UUID para deserialización en las solicitudes post y put)
    id_post    = fields.Str(required=True, load_only=True)     
    usuario    = fields.Nested('UsuarioSchema', exclude=('favoritos',), dump_only=True)  # Relación con Usuario
    post       = fields.Nested('PostSchema', exclude=('favoritos',), dump_only=True)        # Relación con Post

    @post_load
    def make_favorito(self, data, **kwargs):
        # Crear instancia de Favorito asignando campos
        return Favorito(
            id_usuario=data['id_usuario'],
            id_post=data['id_post']
        )