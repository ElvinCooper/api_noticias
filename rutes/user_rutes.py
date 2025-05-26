from flask import request, jsonify, abort
from flask_smorest import Blueprint
from modelos.user_model import Usuario
from schemas.user_simple_schema import UserSimpleSchema
from schemas.user_schema import UserSchema, UserUpdateSchema
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity, create_refresh_token
from extensions import db
from werkzeug.security import check_password_hash, generate_password_hash
from http import HTTPStatus
from marshmallow.exceptions import ValidationError
from datetime import timedelta
from flask_jwt_extended import get_jwt
from modelos.TokenBlocklist_model import TokenBlocklist
from flask.views import MethodView



usuario_bp  = Blueprint('usuarios', __name__, description='Operaciones con Usuarios')
usuario_schema = UserSimpleSchema()
usuarios_schema = UserSimpleSchema(many=True)



# ----------------------------  Consultar todos los usuarios  --------------------------------#
@usuario_bp.route('/usuarios')
class ListarUsuarios(MethodView):
    @jwt_required()
    @usuario_bp.response(HTTPStatus.OK, UserSimpleSchema)
    def get(self):
        usuarios = Usuario.query.all()
        return usuarios 



# --------------------------------- Consultar un usuario por su id ---------------------------------#
@usuario_bp.route('/usuarios/<string:id_usuario>')
class ListarUsuarios(MethodView):
    @jwt_required()    
    @usuario_bp.response(HTTPStatus.OK, UserSimpleSchema)
    def get(self, id_usuario):
        
      usuario = Usuario.query.filter_by(id_usuario=id_usuario).first()
      if not usuario:
          abort(HTTPStatus.NOT_FOUND, message="No existe un usuario con este id")

      return [usuario]


# ---------------------------  Endpoint para Registrar usuarios -----------------------------#
from schemas.user_schema import UserRegisterSchema
@usuario_bp.route("/registrar")
class UsuarioList(MethodView):
   @usuario_bp.arguments(UserRegisterSchema)
   @usuario_bp.response(HTTPStatus.CREATED, UserRegisterSchema)
   def post(self, data_usuario):
      if Usuario.query.filter_by(email=data_usuario.email).first():
         abort(HTTPStatus.BAD_REQUEST, message="Ya existe un usuario con ese email.")

      # hashear el password antes de guardar
      data_usuario.password = generate_password_hash(data_usuario.password)

      db.session.add(data_usuario)
      db.session.commit()

      return data_usuario




# --------------------------------- Actualizar datos de un usuario ---------------------------------#
@usuario_bp.route('/usuarios/<string:id_usuario>')
class UserUpdate(MethodView):
  @usuario_bp.arguments(UserUpdateSchema)
  @usuario_bp.response(HTTPStatus.OK, UserSchema) 
  @jwt_required()
  def put(self, data_usuario, id_usuario):
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
from schemas.user_schema import LoginResponseSchema, LoginSchema
@usuario_bp.route('/login')
class Usuario_Login(MethodView):
    @usuario_bp.arguments(LoginResponseSchema)
    @usuario_bp.response(HTTPStatus.OK, LoginResponseSchema)    
    def post(self, data_login):
        # crear instancia del schema
        login_schema = LoginSchema()
        datos_login = login_schema.load(data_login)

        # Buscar usuario por email
        usuario = Usuario.query.filter_by(email=data_login['email']).first()
        if not usuario:
            abort(HTTPStatus.UNAUTHORIZED, message="Credenciales Invalidas")

        try:
            
          # Generar token de autenticacion
          additional_claims = {"rol": usuario.rol.descripcion}
          acces_token   = create_access_token(identity=usuario.id_usuario, additional_claims=additional_claims)
          refresh_token = create_refresh_token(identity=usuario.id_usuario)

          return { 
              "acces_token": acces_token,
              "refresh_token": refresh_token,
              "usuario": usuario,
              "message": "Login exitoso"
          }
        except Exception as e:
            abort(HTTPStatus.INTERNAL_SERVER_ERROR, message="Error al generar token")            




#------------------ Endpoint para renovar los tokens -------------------#
from schemas.user_schema import TokenRefreshResponseSchema
@usuario_bp.route('/refresh')
class RefreshToken(MethodView):
    @jwt_required()
    @usuario_bp.response(HTTPStatus.OK, TokenRefreshResponseSchema)
    def post(self):
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
from schemas.user_schema import LogoutResponseSchema
@usuario_bp.route('/logout')
class logout(MethodView):
    @jwt_required()
    @usuario_bp.response(HTTPStatus.OK, LogoutResponseSchema)
    def post(self):
        jti =get_jwt['jti']
        db.session.add(TokenBlocklist(jti=jti))
        db.session.commit()
        return {"mensaje": "Sesion cerrada con exito"}
    
    


 # ------------------ Endpoint para obtener usuario actual ------------------
from schemas.user_schema import MeResponseSchema
@usuario_bp.route('/me')
class UsuarioAutenticado(MethodView):
    @jwt_required()
    @usuario_bp.response(HTTPStatus.OK, MeResponseSchema)
    def get(self):
        user_id = get_jwt_identity()
        usuario = Usuario.query.filter_by(id_usuario=user_id).first()

        if not usuario:
            abort(HTTPStatus.NOT_FOUND, message="Usuario no encontrado")

        return usuario_schema.dump(usuario)



#-----------  Endpoint para validar si la solicitud viene del administrador -----------#
from schemas.user_schema import AdminMeSchema
@usuario_bp.route('/admin-only')
class SoloAdmin(MethodView):
  @jwt_required()
  @usuario_bp.response(HTTPStatus.OK, AdminMeSchema)
  def get(self):
      claims = get_jwt()
      if claims.get("rol") != "admin":
          return jsonify({"error": "Acceso denegado"}), HTTPStatus.FORBIDDEN
      
      user_id = get_jwt_identity()
      usuario = Usuario.query.filter_by(id_usuario=user_id).first()
      if not usuario:
          abort(HTTPStatus.NOT_FOUND, message="Usuario no encontrado")

      return usuario
