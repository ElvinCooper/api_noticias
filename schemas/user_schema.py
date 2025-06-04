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
        schema_name = "UserMainSchema"

    id_usuario     = fields.String(dump_only=True)
    nombre         = auto_field(required=True, validate=validate.Length(min=1, max=60))
    email          = fields.Email(required=True) 
    password       = auto_field(required=True, validate=validate.Length(min=8, max=25), load_only=True)
    id_rol         = fields.String(dump_only=True)
    fecha_registro = fields.Date(dump_only=True)
    rol            = fields.Nested(RolSchema, only=('descripcion',), dump_only=True)  # OBjeto Rol relacionado.
    post           = fields.Nested("PostSchema", many=True, dump_only=True)  # Lista de post relacionados
    favoritos      = fields.List(fields.Nested("FavoritoSchema", exclude=('usuario',))) # Lista de favoritos relacionados



#--------------------------------------- Schema base para salida -------------------------------------------------------#
class BaseOutputSchema(SQLAlchemyAutoSchema):
    class Meta:
        load_instance = True
        sqla_session = None
        exclude = ("password", "acces_token", "refresh_token") 
        schema_name="BaseOutputSchema"


# ------------------------  Schema para respuesta a peticion de listar usuarios ---------------------------------#    
class UserSimpleSchema(BaseOutputSchema):
    class Meta:
        model = Usuario        
        sqla_session = db.session
        include_fk = True        
        schema_name = "UserSimpleSchema"
            

    id_usuario = auto_field(dump_only=True)
    nombre = auto_field()
    email = auto_field()
    rol = auto_field()



# ------------------------  Schema para registrar un usuario ---------------------------------#    
class UserRegisterSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Usuario
        load_instance = True
        schema_name = "UserRegisterSchema"

    nombre = fields.String(required=True, validate=validate.Length(min=1, max=60))
    email = fields.Email(required=True)
    password = fields.String(required=True, validate=validate.Length(min=8, max=25), load_only=True)    




# ------------------------  Schema para actualizacion ---------------------------------#    
class UserUpdateSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Usuario
        load_instance = True
        include_relationships = False  # No incluir relaciones en actualización
        sqla_session = db.session
        partial = True 
        schema_name = "UserUpdateSchema"
        fields = ("nombre", "email", "telefono", "password")
    
    # Campos que se pueden actualizar
    nombre = auto_field(required=False, validate=validate.Length(min=1, max=60))
    email = fields.Email(required=False)
    telefono = auto_field(required=False, validate=validate.Length(max=20))
    password = auto_field(required=False, validate=validate.Length(min=8, max=25), load_only=True)




# ------------------------  Schema para recibir datos de Login ---------------------------------#    
class LoginSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Usuario
        load_instance = True
        include_relationships = False  # No incluir relaciones en actualización
        sqla_session = db.session
        partial = True  
        schema_name = "UserLoginSchema"

    email = fields.Email(required=True)
    password = fields.String(required=True, validate=validate.Length(min=1))


# ------------------------  Schema para para respuesta de Login exitoso ---------------------------------#    
class LoginResponseSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Usuario
        load_instance = True
        include_relationships = False  # No incluir relaciones en actualización
        sqla_session = db.session
        partial = True  # Para actualizaciones parciales
        schema_name = "LoginSchema"

    access_token = fields.String()
    refresh_token = fields.String(required=False)  # Si usas refresh tokens
    usuario = fields.Nested(UserSchema, only=('id_usuario', 'nombre', 'email', 'rol'))
    message = fields.String()
    

# --------------------- Schema para la respuesta del refresh token ---------------------------------------#
class TokenRefreshResponseSchema(SQLAlchemyAutoSchema):
    class Meta:
            model = Usuario
            load_instance = True
            include_relationships = False  # No incluir relaciones en actualización
            sqla_session = db.session
            partial = True  # Para actualizaciones parciales
            schema_name = "TokenRefreshSchema"

    acces_token = fields.String(required=True)
    refresh_token = fields.String(required=True)


# --------------------- Schema para la respuesta del Logout ---------------------------------------#
class LogoutResponseSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Usuario
        load_instance = True
        include_relationships = False  # No incluir relaciones en actualización
        sqla_session = db.session
        partial = True  # Para actualizaciones parciales
        schema_name = "UserLogoutSchema"

    mensaje = fields.String()


# --------------------- Schema para la respuesta del usuario autenticado ---------------------------------------#
class MeResponseSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Usuario
        load_instance = True
        include_relationships = False  # No incluir relaciones en actualización
        sqla_session = db.session
        partial = True  # Para actualizaciones parciales
        schema_name = "UserAuthSchema"

    id_usuario = fields.String()
    nombre = fields.String()
    email = fields.Email()
    rol = fields.Nested("RolSchema", only=("descripcion",))


# --------------------- Schema para respuesta del endpoint SoloAdmin --------------------------#

class AdminMeSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Usuario
        load_instance = True
        include_relationships = False  # No incluir relaciones en actualización
        sqla_session = db.session
        partial = True  # Para actualizaciones parciales
        schema_name = "UserAdminSchema"

    id_usuario = fields.String()
    nombre = fields.String()
    email = fields.Email()
    rol = fields.Nested(RolSchema, only=("descripcion",))
    fecha_registro = fields.Date()