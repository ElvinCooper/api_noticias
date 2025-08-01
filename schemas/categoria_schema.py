from marshmallow import fields, validate, post_load
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from modelos.categoria_model import Categoria
from extensions import db


class CategoriaSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Categoria
        load_instance = True
        sqla_session = db.session
        schema_name="CategoriaSchema"
        

    id_categoria  = fields.Str(dump_only=True)
    descripcion   = fields.Str(required=True, validate=validate.Length(max=80))
    eslogan       = fields.Str(allow_none=True)
    id_multimedia = fields.Str(allow_none=True)
    total_publicaciones = fields.Int(dump_only=True)
    

   