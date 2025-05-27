from marshmallow import fields, validate, post_load
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from modelos.post_model import Post
from extensions import db
from schemas.user_schema import UserSchema
from schemas.favorito_schema import FavoritoSchema
from schemas.simple.pais_simple_schema import PaisSimpleSchema
from schemas.categoria_schema import CategoriaSchema
from schemas.multimedia_schema import MultimediaSchema
from extensions import db


class PostSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Post
        load_instance = True
        include_relationships = True
        sqla_session = db.session
        exclude =('favoritos',)

    id_post = fields.Str(dump_only=True)
    titulo  = fields.Str(required=True, validate=validate.Length(max=100))
    contenido = fields.Str(required=True)          
    id_usuario = fields.Str(required=True, load_only=True)
    id_pais = fields.Str(required=True, load_only=True)  # UUID como string para deserialización
    fecha_publicacion = fields.DateTime(dump_only=True)  # Solo para serialización (generado por DB)
    visible = fields.Boolean(load_default=True)  # Por defecto True
    autor = fields.Nested(UserSchema, exclude=('posts',), dump_only=True)  # Relación con Usuario
    pais = fields.Nested(PaisSimpleSchema, dump_only=True)  # Relación con Pais
    favoritos = fields.Nested(FavoritoSchema, many=True, dump_only=True)  # Relación uno a muchos
    
    multimedia = fields.Nested(MultimediaSchema, many=True, dump_only=True)  # Relación uno a muchos
    status    = fields.Boolean(load_default=True) 

    # campo para recibir IDs de categorias desde el cliente.
    categoria_ids = fields.List(fields.Str(), load_only=True, load_default=[])


     # Campos de relaciones, solo para mostrar.
    autor = fields.Nested(UserSchema, exclude=('posts',), dump_only=True)
    pais = fields.Nested(PaisSimpleSchema, dump_only=True)
    favoritos = fields.Nested(FavoritoSchema, many=True, dump_only=True)
    categorias = fields.Nested(CategoriaSchema, many=True, dump_only=True)  # Solo para mostrar
    multimedia = fields.Nested(MultimediaSchema, many=True, dump_only=True)



class PaginationSchema(SQLAlchemyAutoSchema):
    page = fields.Int(load_default=1, validate=lambda x: x >= 1)
    per_page = fields.Int(load_default=10, validate=lambda x: 1 <= x <= 100)

# Schema para la respuesta paginada
class PaginatedPostsSchema(SQLAlchemyAutoSchema):
    posts = fields.Nested(PostSchema, many=True)
    total = fields.Int()
    pages = fields.Int()
    current_page = fields.Int()
    per_page = fields.Int()
    has_next = fields.Bool()
    has_prev = fields.Bool()    