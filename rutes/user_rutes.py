from flask_smorest import Blueprint, abort
from modelos.user_model import Usuario
from modelos.rol_model import Rol
from schemas.user_simple_schema import UserSimpleSchema
from schemas.user_schema import UserSchema, UserUpdateSchema
from schemas.Error_schemas import ErrorSchema
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity, create_refresh_token
from extensions import db
from werkzeug.security import check_password_hash, generate_password_hash
from http import HTTPStatus
from marshmallow.exceptions import ValidationError
from flask_jwt_extended import get_jwt
from modelos.TokenBlocklist_model import TokenBlocklist
from flask.views import MethodView
from flask import current_app
import traceback
import uuid
from datetime import datetime, timezone
from limiter import limiter, require_api_key


# Importacion de Schemas para respuestas de los endpoints
from schemas.user_schema import LoginResponseSchema, LoginSchema
from schemas.user_schema import TokenRefreshResponseSchema
from schemas.user_schema import LogoutResponseSchema
from schemas.user_schema import MeResponseSchema
from schemas.user_schema import AdminMeSchema
from schemas.user_schema import UserRegisterSchema, UserResponseSchema

# Instanciar  el blueprint para las rutas
usuario_bp  = Blueprint('usuarios', __name__, description='Operaciones con Usuarios')



# ----------------------------  CRUD de Usuarios  --------------------------------#
@usuario_bp.route('/usuarios')
class UsuarioResource(MethodView):
    @jwt_required()
    @usuario_bp.response(HTTPStatus.OK, UserSimpleSchema)    
    @usuario_bp.alt_response(HTTPStatus.BAD_REQUEST, schema=ErrorSchema, description="Solicitud inválida", example={"succes": False, "message": "Parametros invalidos"})
    @usuario_bp.alt_response(HTTPStatus.UNAUTHORIZED, schema=ErrorSchema, description="No autorizado", example={"succes": False, "message": "No autorizado"})
    @usuario_bp.alt_response(HTTPStatus.INTERNAL_SERVER_ERROR, schema=ErrorSchema, description="Error interno del servidor", example={"succes": False, "message": "Error interno del servidor"})
    def get(self):
        """ Consultar todos los usuarios """
        usuarios = Usuario.query.all()
        return usuarios 


    @require_api_key()
    @limiter.limit("5 per minute")  # intentos por minuto    
    @usuario_bp.arguments(UserRegisterSchema)
    @usuario_bp.response(HTTPStatus.CREATED, UserResponseSchema)
    @usuario_bp.alt_response(HTTPStatus.BAD_REQUEST, schema=ErrorSchema, description="Ya existe un usuario con ese email", example={"success": False, "message": "Ya existe un usuario con ese email"})
    @usuario_bp.alt_response(HTTPStatus.INTERNAL_SERVER_ERROR, schema=ErrorSchema, description="Error interno del servidor", example={"success": False, "message": "Error interno del servidor"})    
    def post(self, data_usuario):
        """ Registrar un nuevo usuario """
        try:
            current_app.logger.info(f"Datos recibidos: {data_usuario}")
            if Usuario.query.filter_by(email=data_usuario['email']).first():
               return {"success": False, "message": "Ya existe un usuario con ese email."}, HTTPStatus.BAD_REQUEST
            
            
            # if Usuario.query.filter_by(email=data_usuario['email']).first():
            # abort(HTTPStatus.BAD_REQUEST, message="Ya existe un usuario con ese email.")

            # Asignar rol por defecto 
            rol_por_defecto = Rol.query.filter_by(descripcion="usuario").first()
            if not rol_por_defecto:
                rol_por_defecto = Rol(
                id_rol=str(uuid.uuid4()),
                descripcion="usuario"
            )
            db.session.add(rol_por_defecto)
            db.session.commit()
            current_app.logger.info("Rol 'usuario' creado automáticamente.")#abort(HTTPStatus.INTERNAL_SERVER_ERROR, message="No se encontro el predeterminado.")

            # obtener el telefono 
            telefono = data_usuario.get('telefono')

            # Crear el nuevo usuario
            nuevo_usuario = Usuario(
                                    id_usuario=str(uuid.uuid4()),
                                    nombre=data_usuario['nombre'],
                                    email=data_usuario['email'],
                                    password=generate_password_hash(data_usuario['password']),
                                    telefono=telefono,
                                    id_rol=rol_por_defecto.id_rol,
                                    fecha_registro=datetime.now(timezone.utc)
                                )

            # Guardar el nuevo usuario con los datos + rol asignado
            db.session.add(nuevo_usuario)
            db.session.commit()
            
            schema  = UserResponseSchema()
            
            return schema.dump(nuevo_usuario), HTTPStatus.CREATED
        except Exception as e:
            current_app.logger.error(f"Error al registrar usuario: {str(e)}\n{traceback.format_exc()}")
            db.session.rollback()  # Asegurar que la sesión se revierta
            abort(HTTPStatus.INTERNAL_SERVER_ERROR, message=f"Error interno del servidor: {str(e)}")   
    

@usuario_bp.route('/usuarios/<id_usuario>')
class UsuarioUpdateResource(MethodView):
    @usuario_bp.arguments(UserUpdateSchema)
    @usuario_bp.response(HTTPStatus.OK, UserUpdateSchema) 
    @usuario_bp.alt_response(HTTPStatus.NOT_FOUND, schema=ErrorSchema, description="No existe un usuario con este id", example={"success": False, "message": "Not Found"})
    @usuario_bp.alt_response(HTTPStatus.UNAUTHORIZED, schema=ErrorSchema, description="No autorizado", example={"success": False, "message": "No autorizado"})
    @usuario_bp.alt_response(HTTPStatus.INTERNAL_SERVER_ERROR, schema=ErrorSchema, description="Error interno del servidor", example={"success": False, "message": "Error interno del servidor"})
    @jwt_required()
    def put(self, data_usuario, id_usuario):
        """ Actualizar datos de un usuario """
        usuario = Usuario.query.get_or_404(id_usuario, description="Usuario no encontrado")      

        # crear la instancia de actualizacion
        usuario_update_schema = UserUpdateSchema()
        datos_actualizados = usuario_update_schema.load(data_usuario)         

        if 'email' in data_usuario:
            nuevo_email = data_usuario['email']
            # Verificar si ya existe otro usuario con ese email
            existing_user = Usuario.query.filter_by(email=nuevo_email).first()
            
            if existing_user:
                # Si existe, verificar que no sea el mismo usuario
                if existing_user.id_usuario != id_usuario:
                    abort(HTTPStatus.BAD_REQUEST, message="Ya existe un usuario con ese email")
        

        # actualizar los campo del modelo
        usuario.nombre   = datos_actualizados.get('nombre', usuario.nombre)
        usuario.email    = datos_actualizados.get('email',   usuario.email)
        usuario.telefono = datos_actualizados.get('telefono', usuario.telefono)


        try:
            db.session.commit()
            return usuario
        except ValidationError as err:
            db.session.rollback()
            abort (HTTPStatus.INTERNAL_SERVER_ERROR, message="Error al actualizar el usuario")



# -------------------------  Endpoint para hacer Login ------------------------------------#

@usuario_bp.route('/usuarios/login')
class LoginResource(MethodView):
    
    @require_api_key()
    @limiter.limit("10 per minute")
    @usuario_bp.arguments(LoginSchema)
    @usuario_bp.response(HTTPStatus.OK, LoginResponseSchema)
    @usuario_bp.alt_response(HTTPStatus.UNAUTHORIZED, schema=ErrorSchema, description="Credenciales inválidas", example={"success": False, "message": "Credenciales inválidas"})
    @usuario_bp.alt_response(HTTPStatus.INTERNAL_SERVER_ERROR, schema=ErrorSchema, description="Error al generar token", example={"success": False, "message": "Error interno del servidor"})   
    
    def post(self, data_login):
        """ Login de usuarios """        
        try:

            # Buscar usuario por email
            usuario = Usuario.query.filter_by(email=data_login['email']).first()
            if not usuario:
                abort(HTTPStatus.UNAUTHORIZED, message="Credenciales Invalidas")
            
            
            rol_por_defecto = Rol.query.filter_by(descripcion="usuario").first()
            if not rol_por_defecto:
                rol_por_defecto = Rol(
                id_rol=str(uuid.uuid4()),
                descripcion="usuario"
            )
            db.session.add(rol_por_defecto)
            db.session.commit()
            current_app.logger.info("Rol 'usuario' creado automáticamente.")

            # Generar token de autenticacion
            additional_claims = {"rol": usuario.rol.descripcion}
            access_token   = create_access_token(identity=usuario.id_usuario, additional_claims=additional_claims)
            refresh_token = create_refresh_token(identity=usuario.id_usuario)

            response = {
                "access_token": access_token,
                "refresh_token": refresh_token,
                "usuario": {
                    "id_usuario": usuario.id_usuario,
                    "nombre": usuario.nombre,
                    "email": usuario.email,
                    "rol": {"descripcion": usuario.rol.descripcion}
                },
                "message": "Login exitoso"
            }
            schema = LoginResponseSchema()
            return schema.dump(response), HTTPStatus.OK

        except Exception as e:
            current_app.logger.error(f"Error en login: {str(e)}")
            return {"success": False, "message": f"Error interno: {str(e)}"}, HTTPStatus.INTERNAL_SERVER_ERROR

#------------------ Endpoint para renovar los tokens -------------------#
    
@usuario_bp.route('/auth/refresh')
class RefreshToken(MethodView):
    @jwt_required()
    @usuario_bp.response(HTTPStatus.OK, TokenRefreshResponseSchema)
    def post(self):
        """ Renovar los tokens """
        jwt_payload = get_jwt()
        jti = jwt_payload['jti']
        identity = get_jwt_identity()

        # verificar si el token esta revocado
        if TokenBlocklist.query.filter_by(jti=jti).first():
            abort(HTTPStatus.UNAUTHORIZED, message="Refresh token revocado")

        # Revocar el token actual
        db.session.add(TokenBlocklist(jti=jti))
        db.session.commit()

        # Generar nuevos tokens
        new_access_token = create_access_token(identity=identity)
        new_refresh_token = create_refresh_token(identity=identity)

        return {
            "acces_token": new_access_token,
            "refresh_token": new_refresh_token
        }



# ------------------ Endpoint para Logout -----------------------#

@usuario_bp.route('/auth/logout')
class logoutRosource(MethodView):
    @jwt_required()        
    @usuario_bp.response(HTTPStatus.OK, LogoutResponseSchema)
    def post(self):
        """ Logout usuarios  """
        jti =get_jwt['jti']
        db.session.add(TokenBlocklist(jti=jti))
        db.session.commit()
        return {"mensaje": "Sesion cerrada con exito"}
        
        


# ------------------ Endpoint para obtener usuario actual ------------------

@usuario_bp.route('/auth/me')
class AuthResource(MethodView):
    @jwt_required()
    @usuario_bp.response(HTTPStatus.OK, MeResponseSchema)
    def get(self):
        """ Consultar usuarios autenticado """
        user_id = get_jwt_identity()
        usuario = Usuario.query.filter_by(id_usuario=user_id).first()

        if not usuario:
            abort(HTTPStatus.NOT_FOUND, message="Usuario no encontrado")

        return usuario



#-----------  Endpoint para validar si la solicitud viene del administrador -----------#

@usuario_bp.route('/admin/usuarios')
class AdminRosource(MethodView):

    @jwt_required()
    @usuario_bp.response(HTTPStatus.OK, AdminMeSchema)
    def get(self):
        """ Validar usuario administrador """
        claims = get_jwt()
        if claims.get("rol") != "admin":
            abort(HTTPStatus.FORBIDDEN, message="Acceso denegado")
        
        user_id = get_jwt_identity()
        usuario = Usuario.query.filter_by(id_usuario=user_id).first()
        if not usuario:
            abort(HTTPStatus.NOT_FOUND, message="Usuario no encontrado")

        return usuario



# --------------------------------- Consultar un usuario por su id ---------------------------------#
@usuario_bp.route('/usuarios/<string:id_usuario>')
class UsuarioIDResource(MethodView):
    @jwt_required()    

    @usuario_bp.response(HTTPStatus.OK, UserSimpleSchema)
    @usuario_bp.alt_response(HTTPStatus.NOT_FOUND, schema=ErrorSchema, description="No existe un usuario con este id", example={"success": False, "message": "Not Found"})
    @usuario_bp.alt_response(HTTPStatus.UNAUTHORIZED, schema=ErrorSchema, description="No autorizado", example={"success": False, "message": "No autorizado"})
    @usuario_bp.alt_response(HTTPStatus.INTERNAL_SERVER_ERROR, schema=ErrorSchema, description="Error interno del servidor", example={"success": False, "message": "Error interno del servidor"})
    def get(self, id_usuario):
      """ Consultar un usuario por su ID """
        
      usuario = Usuario.query.filter_by(id_usuario=id_usuario).first()
      if not usuario:
          abort(HTTPStatus.NOT_FOUND, message="No existe un usuario con este id")

      return usuario
 











    




