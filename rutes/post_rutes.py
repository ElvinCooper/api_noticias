from flask import Blueprint, request, jsonify
from modelos.post_model import Post
from schemas.categoria_schema import CategoriaSchema
from schemas.post_schema import PostSchema
from schemas.pais_schema import PaisSchema
from schemas.favorito_schema import FavoritoSchema
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


#---------------------- Enpoint para consultar todos los post en la BD --------------------------#
@post_bp.route('/post', methods=['GET'])
@jwt_required() 
def get_all_post():
  """
    Obtener todos los posts
    ---
    tags:
      - Posts
    responses:
      200:
        description: Lista de posts
        schema:
          type: array
          items:
            $ref: '#/definitions/Post'
  """
  posts = Post.query.all()
  return jsonify(posts_schemas.dump(posts)), HTTPStatus.OK





#------------------------ Enpoint consultar un post con su id ----------------------#
@post_bp.route('/<string:id_post>', methods=['GET'])
def get_post(id_post):
    """
    Obtener un post por ID

    Retorna los detalles de un post específico según su ID.
    ---
    tags:
      - Posts
    parameters:
      - name: id_post
        in: path
        type: string
        required: true
        description: ID del post
    responses:
      200:
        description: Post encontrado
        schema:
          $ref: '#/definitions/Post'
      404:
        description: Post no encontrado
    """
    post = Post.query.get_or_404(id_post)

    return jsonify(post_schema.dump(post)), HTTPStatus.OK



# ---------------------------  Endpoint para crear un nuevo Post -----------------------------#
@post_bp.route('/create', methods=['POST'])
@jwt_required()
def crear_post():
    
  """
  Crear un nuevo post

  Permite a un usuario autenticado crear un nuevo post.
  ---
  tags:
    - Posts
  security:
    - BearerAuth: []
  parameters:
    - name: body
      in: body
      required: true
      schema:
        $ref: '#/definitions/Post'
  responses:
    201:
      description: Post creado exitosamente
      schema:
        $ref: '#/definitions/Post'
    400:
      description: Error al crear el post
  """

    
  json_data = request.get_json()
  user_id = get_jwt_identity()
  
  try:
    json_data['id_usuario'] = user_id
    nuevo_post = post_schema.load(json_data)
    db.session.add(nuevo_post)
    db.session.commit()
    return jsonify(post_schema.dump(nuevo_post)), HTTPStatus.CREATED
  except Exception as e:
      db.session.rollback()
      return jsonify({'error': str(e)}), HTTPStatus.BAD_REQUEST





# ------------------------ Endpoint para eliminar un Post ---------------------------- #
@post_bp.route('/del/<string:id_post>', methods=['DELETE'])
@jwt_required()
def eliminar_post(id_post):
    """
    Eliminar un post

    Permite a un usuario autenticado eliminar su propio post.
    ---
    tags:
      - Posts
    security:
      - BearerAuth: []
    parameters:
      - name: id_post
        in: path
        type: string
        required: true
        description: ID del post a eliminar
    responses:
      200:
        description: Post eliminado exitosamente
      403:
        description: No tienes permisos para eliminar este post
      404:
        description: Post no encontrado
    """
    id_usuario = get_jwt_identity()
    post = Post.query.get(id_post)

    if not post:
        return jsonify({"mensaje": "Post no encontrado"}), HTTPStatus.NOT_FOUND

    if post.id_usuario != id_usuario:
        return jsonify({"mensaje": "No tienes permisos para eliminar este post"}), HTTPStatus.FORBIDDEN

    db.session.delete(post)
    db.session.commit()
    return jsonify({"mensaje": "Post eliminado exitosamente"}), HTTPStatus.OK



