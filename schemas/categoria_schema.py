from marshmallow import fields, validate, post_load
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from modelos.categoria_model import Categoria



class CategoriaSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Categoria
        load_instance = True
        exclude = ('multimedia',)

    id_categoria  = fields.Str(dump_only=True)
    descripcion   = fields.Str(required=True, validate=validate.Length(50))
    id_multimedia = fields.Str(allow_none=True, load_only=True)
    multimedia    = fields.Nested("MultimediaSchema", exclude=('categoria', 'pais'), dump_only=True)

    @post_load
    def make_categoria(self, data, **kwargs):
        return Categoria(
            descripcion=data['descripcion'],
            id_multimedia=data.get('id_multimedia')
        )