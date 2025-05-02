from flask import Blueprint, request, jsonify
from modelos.post_model import Post
from modelos.categoria_model import Categoria
from schemas.post_schema import PostSchema
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from extensions import db
from werkzeug.security import check_password_hash, generate_password_hash
from http import HTTPStatus
from marshmallow.exceptions import ValidationError
from datetime import timedelta, timezone




post_bp = Blueprint('post', __name__)

# Esquemas para Serializacion/Deserializacion
post_schema = PostSchema()
posts_schemas = PostSchema(many=True)


#---------------------- Enpoint para leer todos los post --------------------------#
@post_bp.route('/', methods=['GET'])
def get_posts():
    '''
    docstring
    '''
    post = Post.query.all()
    return jsonify(posts_schemas.dump(post)), HTTPStatus.OK


#------------------------ Enpoint consultar un post con su id ----------------------#
@post_bp.route('/<String:id_post>', methods=['GET'])
def get_post(id_post):
    '''
    docstring
    '''
    post = Post.query.get_or_404(id_post)

    return jsonify(post_schema.dump(post)), HTTPStatus.OK



# ---------------------------  Endpoint para Registrar un Post -----------------------------#
@post_bp.route('/', methods=['POST'])
@jwt_required()
def crear_post():
    '''
     """
    Registro de un Post

    Este endpoint permite a un usuario registrarse en proveeyendo
    un username, correo y contraseña.
    '''
    json_data = request.get_json()
    user_id = get_jwt_identity()
    
    try:
        nuevo_post = post_schema.load(json_data)
        post = Post(titulo=nuevo_post['titulo'],
                    contenido=nuevo_post['contenido'],
                    id_pais=nuevo_post['id_pais'],
                    visible=nuevo_post.get('visible', True), # valor por defecto
                    status=nuevo_post.get('status', True), # valor por defecto
                     id_usuario=user_id)   # viene del token
        
        db.session.add(post)
        db.session.commit()
        return jsonify(post_schema.dump(post)), HTTPStatus.CREATED
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), HTTPStatus.BAD_REQUEST