from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from modelos.favorito_model import Favorito
from modelos.post_model import Post
from extensions import db
from http import HTTPStatus

favorito_bp = Blueprint('favoritos', __name__)



# ------------------- Endpoint para ver todos los post favoritos --------------------------#
@favorito_bp.route('/', methods=['GET'])
@jwt_required()
def obtener_favoritos_usuario():
    """
    Obtener posts favoritos del usuario autenticado
    ---
    tags:
      - Favoritos
    security:
      - BearerAuth: []
    responses:
      200:
        description: Lista de posts favoritos
        schema:
          type: array
          items:
            $ref: '#/definitions/Post'
    """
    id_usuario = get_jwt_identity()
    favoritos = Favorito.query.filter_by(id_usuario=id_usuario).all()
    
    posts = [fav.post for fav in favoritos]  # accedemos a los objetos Post relacionados

    from schemas.post_schema import PostSchema  # asegúrate de tener un esquema para Post
    post_schema = PostSchema(many=True)
    
    return jsonify(post_schema.dump(posts)), HTTPStatus.OK



# ------------------- Endpoint para ver favoritos de otro usuario por si ID --------------------------#

@favorito_bp.route('/usuario/<string:id_usuario>', methods=['GET'])
def favoritos_por_usuario(id_usuario):
    """
    Obtener favoritos de un usuario por su ID
    ---
    tags:
      - Favoritos
    parameters:
      - name: id_usuario
        in: path
        required: true
        type: string
        description: ID del usuario
    responses:
      200:
        description: Lista de posts favoritos del usuario
        schema:
          type: array
          items:
            $ref: '#/definitions/Post'
    """
    favoritos = Favorito.query.filter_by(id_usuario=id_usuario).all()
    posts = [fav.post for fav in favoritos]

    from schemas.post_schema import PostSchema
    post_schema = PostSchema(many=True)

    return jsonify(post_schema.dump(posts)), HTTPStatus.OK




#------------------  Enpoint para marcar un post como favorito ----------------------#

@favorito_bp.route('/', methods=['POST'])
@jwt_required()
def crear_favorito():
    """
    Marcar un post como favorito
    ---
    tags:
      - Favoritos
    security:
      - BearerAuth: []
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          required:
            - id_post
          properties:
            id_post:
              type: integer
              description: ID del post a marcar como favorito
    responses:
      201:
        description: Post agregado a favoritos exitosamente
        schema:
          $ref: '#/definitions/Post'
      400:
        description: Falta el campo 'id_post'
      404:
        description: Post no encontrado
      409:
        description: Post ya está en favoritos
    """
    json_data = request.get_json()
    id_post = json_data.get('id_post')
    id_usuario = get_jwt_identity()

    if not id_post:
        return jsonify({"error": "El campo 'id_post' es obligatorio"}), HTTPStatus.BAD_REQUEST

    # Validar que el post existe
    post = Post.query.get(id_post)
    if not post:
        return jsonify({"error": "El post no existe"}), HTTPStatus.NOT_FOUND

    # Validar que no se haya marcado como favorito antes
    favorito_existente = Favorito.query.filter_by(id_usuario=id_usuario, id_post=id_post).first()
    if favorito_existente:
        return jsonify({"mensaje": "Este post ya está en tus favoritos"}), HTTPStatus.CONFLICT


    # Crear nuevo favorito
    nuevo_favorito = Favorito(id_usuario=id_usuario, id_post=id_post)
    db.session.add(nuevo_favorito)
    db.session.commit()

    return jsonify({
        "mensaje": "Post agregado a favoritos exitosamente",
        "id_usuario": id_usuario,
        "id_post": id_post
    }), HTTPStatus.CREATED



#------------------------------------ Enpoint para eliminar un favorito ---------------------------------------#

@favorito_bp.route('/<string:id_post>', methods=['DELETE'])
@jwt_required()
def eliminar_favorito(id_post):
    """
    Eliminar un post de los favoritos del usuario
    ---
    tags:
      - Favoritos
    security:
      - BearerAuth: []
    parameters:
      - name: id_post
        in: path
        required: true
        type: string
        description: ID del post a eliminar de favoritos
        schema:
          $ref: '#/definitions/Favorito'
    responses:
      200:
        description: Post eliminado de favoritos
      404:
        description: El post no estaba en tus favoritos
    """
    id_usuario = get_jwt_identity()
    
    favorito = Favorito.query.filter_by(id_usuario=id_usuario, id_post=id_post).first()
    if not favorito:
        return jsonify({"mensaje": "Este post no está en tus favoritos"}), HTTPStatus.NOT_FOUND

    db.session.delete(favorito)
    db.session.commit()

    return jsonify({"mensaje": "Post eliminado de tus favoritos"}), HTTPStatus.OK


