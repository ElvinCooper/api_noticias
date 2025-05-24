# schemas/user_simple_schema.py
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from modelos.user_model import Usuario
from marshmallow import fields
from extensions import db
class UserSimpleSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Usuario
        load_instance = True
        sqla_session = db.session

    id_usuario = fields.Str()
    nombre = fields.Str()
    email = fields.Email()
