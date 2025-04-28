from marshmallow import fields, validate
from marshmallow_sqlalchemy import SQLAlchemyAutoshchema, auto_field
from modelos.user_model import Usuario


class UserSchema(SQLAlchemyAutoshchema):
    class Meta:
        model = Usuario
        load_instance = True
        include_relationships = True

    id_usuario     = fields.String(dump_only=True)
    nombre         = auto_field(required=True, validate=validate.Length(min=1, max=60))
    email          = fields.Email(required=True) 
    password       = auto_field(required=True, validate=validate.Length(min=8, max=25))
    id_rol         = fields.String(dump_only=True)
    fecha_registro = fields.Date(dump_only=True)
    rol            = fields.Nested('Rolschema', exclude=('usuarios',))  # OBjeto Rol relacionado.
    post           = fields.List(fields.Nested('Postschema', exclude=('usuario,'))) # lista de post relacionados
    favoritos      = fields.List(fields.Nested('Favoritoschema', exclude=('usuario')))