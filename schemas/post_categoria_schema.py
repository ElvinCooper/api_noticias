from marshmallow import fields, post_load
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from modelos.post_categoria_model import PostCategoria
from extensions import db

class PostCategoriaSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = PostCategoria
        load_instance = True
        include_relationships = True
        sqla_session = db.session

    id_post      = fields.Str(required=True, load_only=True)
    id_categoria = fields.Str(required=True, load_only=True)

    

