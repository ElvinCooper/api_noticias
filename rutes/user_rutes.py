from flask import Blueprint, request, jsonify
from modelos.user_model import Usuario
from schemas.user_schema import UserSchema
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from extensions import db
from werkzeug.security import check_password_hash, generate_password_hash
from http import HTTPStatus
from marshmallow.exceptions import ValidationError
from datetime import timedelta



usuario_bp  = Blueprint('usuarios', __name__)
usuario_schema = UserSchema()
usuarios_schema = UserSchema(many=True)




# ----------------------------  Consultar todos los usuarios  --------------------------------#
@usuario_bp.route('/', methods=['GET'])
def get_usuarios():
    '''
    En este endpoint se visualizan todos los usuarios en la db
    '''
    usuarios = Usuario.query.all()
    return jsonify(usuarios_schema.dumps(usuarios)), HTTPStatus.OK


# --------------------------------- Consultar un usuario por su id ---------------------------------#
@usuario_bp.route('/<String:id_usuario>', methods=['GET'])
def get_usuario(id_usuario):
    usuario = Usuario.query.get_or_404(id_usuario)
    return jsonify(usuario_schema.dumps(usuario)), HTTPStatus.OK



# ---------------------------  Endpoint para Registrar usuarios -----------------------------#
@usuario_bp.route('/registro', methods=['POST'])
def crear_usuario():
    '''
     """
    Registro de usuario

    Este endpoint permite a un usuario registrarse en proveeyendo
    un username, correo y contraseña.
    '''
    try:
        data = request.get_json()
        nombre = data.get('nombre')
        email  = data.get('email')
        password = data.get('password')
        id_rol = data.get('id_rol')

        # Verificar si todos los campos existen
        if not all([nombre, email, password, id_rol]):
            return jsonify({"mensaje": "Faltan alguno de los campos, favor revisar"}), HTTPStatus.BAD_REQUEST
        
        # Validar duplicados
        if Usuario.query.filter_by(email-email).first():
            return jsonify({"mensaje": "Ya existe un usuario con este email"}), HTTPStatus.BAD_REQUEST
        
        # Creacion del usuario
        nuevo_usuario = Usuario(nombre= nombre,
                                email = email,
                                password=generate_password_hash(password),
                                id_rol = id_rol)
        
        db.session.add(nuevo_usuario)
        db.session.commit()

        # Futura Logico de envio de correo en esta parte
          


        return jsonify(usuario_schema.dump(nuevo_usuario)), HTTPStatus.CREATED        
    
    except ValidationError as err:
        return jsonify({"error": err.messages}), HTTPStatus.BAD_REQUEST



# -------------------------  Endpoint para hacer Login ------------------------------------#
@usuario_bp.route('/login', methods=['POST'])
def login():
    '''
    docstring
    
    '''
    json_data = request.get_json()
    email    = json_data.get('email')
    password = json_data.get('password')


    # Validar el usuario 
    usuario = Usuario.query.filter.by(email=email).first()
    if not usuario:
        return jsonify({"mensaje": "Este usuario no existe en la base de datos"}), HTTPStatus.NOT_FOUND
    
    # Validar password
    if not check_password_hash(usuario.password, password):
        return jsonify({"mensaje": "Credenciales invalidas"}), HTTPStatus.UNAUTHORIZED
    
    # Generar token de autenticacion
    acces_token = create_access_token(identity=usuario.id, expires_delta=timedelta(hours=2))


    # Logica de envio de correos


    return jsonify({"mensaje": "Login exitoso",
                    "acces_token": acces_token}), HTTPStatus.OK



 # ------------------------------ Enpoint para obtener el usuario logueado --------------------------------#
@usuario_bp.route('/me', methods=['GET'])
@jwt_required()
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
          id: Usuario
          properties:
            id:
              type: integer
            username:
              type: string
      404:
        description: Usuario no encontrado
    """    
    user_id = get_jwt_identity()  # Extrae el 'identity' del JWT
    usuario = Usuario.query.filter_by(id=user_id).first()

    if not usuario:
        return jsonify({"error": "Usuario no encontrado"}), HTTPStatus.NOT_FOUND

    return jsonify(usuario_schema.dump(usuario)), HTTPStatus.OK