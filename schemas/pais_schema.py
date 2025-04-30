from marshmallow import fields, validate, post_load
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from modelos.pais_model import Pais



class PaisSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Pais
        load_instance = True
        include_relationships = True


    id_pais = fields.Str(dump_only=True)
    nombre_pais      = fields.Str(required=True, validate=validate.Length(max=(50)))
    abrebiatura_pais = fields.Str(required=True, validate=validate.Length(3))
    id_multimedia    = fields.Str(allow_none=True, load_only=True)
    multimedia       = fields.Nested('MultimediaSchema', exclude=('pais', 'categoria'), dump_only=True)

    @post_load
    def make_pais(self, data, **kwargs):
        return Pais(
            nombre_pais=data['nombre_pais'],
            abrebiatura_pais=data['abrebiatura_pais'],
            id_multimedia=data.get('id_multimedia')
        )