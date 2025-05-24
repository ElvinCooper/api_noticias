from flask import request, jsonify
from flask_smorest import Blueprint
from modelos.user_model import Usuario
from schemas.user_simple_schema import UserSimpleSchema
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity, create_refresh_token
from extensions import db
from werkzeug.security import check_password_hash, generate_password_hash
from http import HTTPStatus
from marshmallow.exceptions import ValidationError
from datetime import timedelta
from flask_jwt_extended import get_jwt
from modelos.TokenBlocklist_model import TokenBlocklist



usuario_bp  = Blueprint('usuarios', __name__, description='Operaciones con Usuarios')
usuario_schema = UserSimpleSchema()
usuarios_schema = UserSimpleSchema(many=True)




# ----------------------------  Consultar todos los usuarios  --------------------------------#
@usuario_bp.route('/users', methods=['GET'])
def get_usuarios():
    """
    Obtener todos los usuarios

    Este endpoint retorna la lista de todos los usuarios registrados en el sistema.
    ---
    tags:
      - Usuarios
    responses:
      200:
        description: Lista de usuarios
        schema:
           $ref: '#/definitions/Usuario'
    """
    usuarios = Usuario.query.all()
    return jsonify(usuarios_schema.dumps(usuarios)), HTTPStatus.OK



# --------------------------------- Consultar un usuario por su id ---------------------------------#
@usuario_bp.route('/<string:id_usuario>', methods=['GET'])
#@jwt_required()
def get_usuario(id_usuario):
    """
        Obtener usuario por ID

        Retorna los datos de un usuario específico usando su ID.
        ---
        tags:
          - Usuarios
        parameters:
          - name: id_usuario
            in: path
            type: string
            required: true
            description: ID del usuario a consultar
        responses:
          200:
            description: Usuario encontrado
            schema:
              $ref: '#/definitions/Usuario'
          404:
            description: Usuario no encontrado
        """    
    usuario = Usuario.query.get_or_404(id_usuario)
    if not usuario:
        return jsonify({"error": "Usuario no encontrado"}), HTTPStatus.NOT_FOUND
    
    return jsonify(usuario_schema.dumps(usuario)), HTTPStatus.OK



# ---------------------------  Endpoint para Registrar usuarios -----------------------------#
@usuario_bp.route('/registro', methods=['POST'])
def crear_usuario():
    """
      Registro de nuevo usuario

      Permite registrar un nuevo usuario con nombre, email, contraseña e ID de rol.
      ---
      tags:
        - Usuarios
      parameters:
        - name: body
          in: body
          required: true
          schema:
            $ref: '#/definitions/RegistroUsuario'
      responses:
        201:
          description: Usuario creado exitosamente
          schema:
            $ref: '#/definitions/RegistroUsuario'
        400:
          description: Datos inválidos o incompletos
      """
    try:
        data = request.get_json()
        nombre = data.get('nombre')
        email  = data.get('email')
        telefono = data.get('telefono')
        password = data.get('password')
        id_rol = data.get('id_rol')

        # Verificar si todos los campos existen
        if not all([nombre, email, password, id_rol]):
            return jsonify({"mensaje": "Faltan alguno de los campos, favor revisar"}), HTTPStatus.BAD_REQUEST
        
        # Validar duplicados
        if Usuario.query.filter_by(email = email).first():
            return jsonify({"mensaje": "Ya existe un usuario con este email"}), HTTPStatus.BAD_REQUEST
        
        # Creacion del usuario
        nuevo_usuario = Usuario(nombre   = nombre,
                                email    = email,
                                telefono = telefono,
                                password = generate_password_hash(password),
                                id_rol   = id_rol)
        
        db.session.add(nuevo_usuario)
        db.session.commit()

        # Futura Logico de envio de correo en esta parte
          


        return jsonify(usuario_schema.dump(nuevo_usuario)), HTTPStatus.CREATED        
    
    except ValidationError as err:
        return jsonify({"error": err.messages}), HTTPStatus.BAD_REQUEST



# --------------------------------- Actualizar datos de un usuario ---------------------------------#
@usuario_bp.route('/update/<string:id_usuario>', methods=['PUT'])
#@jwt_required()
def actualizar_usuario(id_usuario):
    """
      Permite a un usuario autenticado actualizar sus datos como nombre, email y numero telefonico.

      ---
      tags:
        - Usuarios
      parameters:
        - name: body
          in: body
          required: true
          schema:
            $ref: '#/definitions/ActualizarUsuario'
      responses:
        201:
          description: Usuario actualizado exitosamente
          schema:
            $ref: '#/definitions/ActualizarUsuario'
        404:
          description: Usuario no encontrado
        403:
          description: No autorizado. Solo administradores pueden realizar esta acción.
        400:
          description: No hay datos proporcinados.  
      """    
     
    id_usuario = get_jwt_identity()

    admin_id = get_jwt_identity()
    admin_user = db.session.get(Usuario, admin_id)
    
    if not admin_user or admin_user.rol != 'admin':
      return jsonify({"error": "No autorizado. Solo administradores pueden realizar esta acción."}), HTTPStatus.FORBIDDEN
    
    usuario = db.session.get(Usuario, id_usuario)

    if not usuario:
        return jsonify({"error": "Usuario no encontrado"}), HTTPStatus.NOT_FOUND
    
    try:
      json_data = request.get_json()
      if not json_data:
        return jsonify({"mensaje":"No hay datos proporcinados"}), HTTPStatus.BAD_REQUEST
      
      # verificar si ya existe un usuario con el mismo email
      if Usuario.query.filter_by(email=json_data.email).first():        
        return jsonify({"mensaje": "Ya existe un contacto con este email"}), HTTPStatus.BAD_REQUEST
      
      datos_actualizados = usuario_schema.load(json_data, session=db.session, partial=True)

      db.session.commit()
      return jsonify(usuario_schema.dump(datos_actualizados)), HTTPStatus.OK

    except ValidationError as e:
      return jsonify({"error": e.messages}), HTTPStatus.BAD_REQUEST
    except Exception as err:
      return jsonify({"error": str(err)}), HTTPStatus.BAD_REQUEST  



# -------------------------  Endpoint para hacer Login ------------------------------------#
@usuario_bp.route('/login', methods=['POST'])
def login():
    """
    Login de usuario

    Permite a un usuario autenticarse usando su email y contraseña. Retorna un token JWT si es exitoso.
    ---
    tags:
      - Usuarios
    parameters:
      - name: body
        in: body
        required: true
        schema:
         $ref: '#/definitions/LoginUsuario'
    responses:
      200:
        description: Login exitoso con token JWT
        schema:
          $ref: '#/definitions/LoginUsuario'
      401:
        description: Credenciales inválidas
      404:
        description: Usuario no encontrado
    """
    json_data = request.get_json()
    email    = json_data.get('email')
    password = json_data.get('password')


    # Validar el usuario 
    usuario = Usuario.query.filter_by(email=email).first()
    if not usuario:
        return jsonify({"mensaje": "Este usuario no existe en la base de datos"}), HTTPStatus.NOT_FOUND
    
    # Validar password
    if not check_password_hash(usuario.password, password):
        return jsonify({"mensaje": "Credenciales invalidas"}), HTTPStatus.UNAUTHORIZED
    
    rol = usuario.rol.descripcion if usuario.rol else "sin_rol_definido" # ← Obtener el nombre del rol (ej. 'admin')

    # Generar token de autenticacion
    acces_token = create_access_token(identity=usuario.id_usuario, additional_claims={"rol": rol})
    refresh_token = create_refresh_token(identity=usuario.id_usuario)


    return jsonify({"mensaje": "Login exitoso",
                    "acces_token": acces_token,
                    "refresh_token": refresh_token,
                    }), HTTPStatus.OK



#------------------ Endpoint para renovar los tokens -------------------#
@usuario_bp.route('/refresh', methods=['POST'])
#@jwt_required(refresh=True) # solo acepta refresh tokens
def refresh():
    """
    Renovación de tokens JWT (Access y Refresh)

    Este endpoint permite a un usuario autenticado con un token de actualización (refresh token) obtener
    un nuevo par de tokens JWT. El refresh token utilizado se revoca inmediatamente después de ser usado, 
    implementando una política de rotación segura.

    ---
    tags:
      - Usuarios
    security:
      - BearerAuth: []
    responses:
      200:
        description: Nuevos tokens JWT generados exitosamente
        schema:
          $ref: '#/definitions/RefreshTokenResponse'
      401:
        description: El refresh token ha sido revocado o es inválido
    """    
    jwt_payload = get_jwt()
    jti = jwt_payload['jti'] # id del token actual
    identity = get_jwt_identity() # id del usuario

    # validar si ya el token fue revocado
    token_revocado = TokenBlocklist.query.filter_by(jti=jti).first()
    if token_revocado:
        return jsonify({"mensaje": "Refresh token revocado"}), HTTPStatus.UNAUTHORIZED
    
    # Revocar token actual (guardando en el blocklist)
    db.session.add(TokenBlocklist(jti=jti))
    db.session.commit()

    # Emitir nuevo acces y refresh token
    new_acces_token = get_jwt_identity()
    new_refresh_token = create_refresh_token(identity=identity)

    return jsonify({"acces_token": new_acces_token,
                    "refresh_token": new_refresh_token,}), HTTPStatus.OK



# ------------------ Endpoint para Logout -----------------------#
@usuario_bp.route('/logout', methods=['POST'])
#@jwt_required()
def logout():
  """
  Cerrar sesión

  Revoca el token JWT actual agregándolo a la blocklist.
  ---
  tags:
    - Usuarios
  security:
    - BearerAuth: []
  responses:
    200:
      description: Sesión cerrada exitosamente
    401:
      description: Token inválido o ya revocado
  """
  jti = get_jwt()["jti"]  # Para extraer el ID único del token
  db.session.add(TokenBlocklist(jti=jti))
  db.session.commit()
  return jsonify({"mensaje": "Sesión cerrada con éxito"}), HTTPStatus.OK



 # ------------------------------ Enpoint para obtener el usuario logueado --------------------------------#
@usuario_bp.route('/me', methods=['GET'])
#@jwt_required()
def obtener_usuario_autenticado():
    """
    Obtener usuario autenticado

    Este endpoint permite un usuario autenticado consultar 
    la informacion del usuario que esta logueado en ese momento.
    ---
    tags:
      - Usuarios
    security:
      - BearerAuth: []
    responses:
      200:
        description: Datos del usuario autenticado
        schema:
          $ref: '#/definitions/Usuario'
      404:
        description: Usuario no encontrado
    """    
    user_id = get_jwt_identity()  # Extrae el 'identity' del JWT
    usuario = Usuario.query.filter_by(id_usuario=user_id).first()

    if not usuario:
        return jsonify({"error": "Usuario no encontrado"}), HTTPStatus.NOT_FOUND

    return jsonify(usuario_schema.dump(usuario)), HTTPStatus.OK




#-----------  Endpoint para validar si la solicitud viene del administrador -----------#
#@jwt_required()
def endpoint_solo_admin():
    claims = get_jwt()
    if claims.get("rol") != "admin":
        return jsonify({"error": "Acceso denegado"}), 403

    return jsonify({"mensaje": "Bienvenido administrador"}), 200
