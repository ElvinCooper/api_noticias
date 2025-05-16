# schemas/pais_simple_schema.py
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from modelos.pais_model import Pais
from marshmallow import fields

class PaisSimpleSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Pais
        load_instance = True
        exclude = ('multimedia',)

    id_pais = fields.Str()
    nombre_pais = fields.Str()
    abrebiatura_pais = fields.Str()
