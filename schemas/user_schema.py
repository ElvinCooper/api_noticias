from marshmallow import fields, validate
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema, auto_field
from modelos.user_model import Usuario
from schemas.rol_schema import RolSchema
from extensions import db


class UserSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Usuario
        load_instance = True
        include_relationships = True
        sqla_session = db.session

    id_usuario     = fields.String(dump_only=True)
    nombre         = auto_field(required=True, validate=validate.Length(min=1, max=60))
    email          = fields.Email(required=True) 
    password       = auto_field(required=True, validate=validate.Length(min=8, max=25), load_only=True)
    id_rol         = fields.String(dump_only=True)
    fecha_registro = fields.Date(dump_only=True)
    rol            = fields.Nested(RolSchema, only=('descripcion',), dump_only=True)  # OBjeto Rol relacionado.
    post           = fields.Nested("PostSchema", many=True, dump_only=True)  # Lista de post relacionados
    favoritos      = fields.List(fields.Nested("FavoritoSchema", exclude=('usuario',))) # Lista de favoritos relacionados

    