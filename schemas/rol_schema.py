from marshmallow import fields, validate, post_load
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from modelos.rol_model import Rol
from extensions import db

class RolSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Rol
        load_instance = True
        #include_relationships = True
        exclude = ('usuarios',)
        sqla_session = db.session        
        schema_name="RolSchema"

        id_rol = fields.String(dump_only=True)
        descripcion = fields.String(required=True, validate=validate.Length(min=10, max=120))
        usuarios    = fields.Nested("UserSchema", many=True, only=("id_usuario", "nombre", "email"),dump_only=True)

       


