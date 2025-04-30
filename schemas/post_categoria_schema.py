from marshmallow import fields, post_load
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from modelos.post_categoria_model import PostCategoria


class PostCategoriaSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = PostCategoria
        load_instance = True
        include_relationships = True

    id_post      = fields.Str(required=True, load_only=True)
    id_categoria = fields.Str(required=True, load_only=True)

    @post_load
    def make_post_categoria(self, data, **kwargs):
        return PostCategoria(
            id_post=data['id_post'],
            id_categoria=data['id_categoria']
        )

