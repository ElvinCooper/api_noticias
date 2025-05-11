from marshmallow import fields, validate, post_load
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from modelos.post_model import Post
from extensions import db



class PostSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Post
        load_instance = True
        include_relationships = True
        sqla_session = db.session

    id_post = fields.Str(dump_only=True)
    titulo  = fields.Str(required=True, validate=validate.Length(max=100))
    contenido = fields.Str(required=True)          
    id_usuario = fields.Str(required=True, load_only=True)
    id_pais = fields.Str(required=True, load_only=True)  # UUID como string para deserialización
    fecha_publicacion = fields.DateTime(dump_only=True)  # Solo para serialización (generado por DB)
    visible = fields.Boolean(load_default=True)  # Por defecto True
    autor = fields.Nested('UserSchema', exclude=('posts',), dump_only=True)  # Relación con Usuario
    pais = fields.Nested("PaisSchema", exclude=('posts',), dump_only=True)  # Relación con Pais
    categorias = fields.Nested("CategoriaSchema", many=True, dump_only=True)  # Relación muchos a muchos
    multimedia = fields.Nested("MultimediaSchema", many=True, dump_only=True)  # Relación uno a muchos
    favoritos = fields.Nested("FavoritoSchema", many=True, dump_only=True)  # Relación uno a muchos
    status    = fields.Boolean(load_default=True) 

    #@post_load
    def make_post(self, data, **kwargs):
        # Crear instancia de Post asignando campos manualmente
        return Post(
            titulo=data['titulo'],
            contenido=data['contenido'],
            id_usuario=data['id_usuario'],
            id_pais=data['id_pais'],
            visible=data.get('visible', True)
        )