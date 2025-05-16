from marshmallow import fields, validate, post_load
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from modelos.rol_model import Rol


class RolSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Rol
        load_instance = True
        #include_relationships = True
        exclude = ('usuarios',)

        id_rol = fields.String(dump_only=True)
        descripcion = fields.String(required=True, validate=validate.Length(min=10, max=120))
        usuarios    = fields.Nested('UserSchema', many=True, exclude=('rol',),dump_only=True)

        @post_load
        def make_role(self, data, **kwargs):
            return Rol(id_rol=data)


