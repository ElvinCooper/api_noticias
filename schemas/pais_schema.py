from marshmallow import fields, validate, post_load
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from modelos.pais_model import Pais
from schemas.multimedia_schema import MultimediaSchema
from extensions import db


class PaisSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Pais
        load_instance = True
        sqla_session = db.session
        

    id_pais = fields.Str(dump_only=True)
    nombre_pais      = fields.Str(required=True, validate=validate.Length(max=(50)))
    abrebiatura_pais = fields.Str(required=True, validate=validate.Length(3))
    id_multimedia    = fields.Str(allow_none=True, load_only=True)
    

class PaisCreateSchema(SQLAlchemyAutoSchema):
    id_pais = fields.Str(required=True)
    nombre_pais = fields.Str(required=True, validate=validate.Length(max=50))
    abrebiatura_pais = fields.Str(required=True, validate=validate.Length(equal=3))    