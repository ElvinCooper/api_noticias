from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from modelos.post_model import Post
from extensions import db
from marshmallow import fields

class PostSimpleSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Post
        load_instance = True
        sqla_session = db.session
        exclude = ()  # sin relaciones

    id_post = fields.Str(dump_only=True)
    titulo = fields.Str()
    contenido = fields.Str()
    fecha_publicacion = fields.DateTime()
    visible = fields.Boolean()
