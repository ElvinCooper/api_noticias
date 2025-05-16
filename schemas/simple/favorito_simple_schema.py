from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from modelos.favorito_model import Favorito
from extensions import db
from marshmallow import fields

class FavoritoSimpleSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Favorito
        load_instance = True
        sqla_session = db.session
        include_relationships = False

    id_usuario = fields.Str()
    id_post = fields.Str()
