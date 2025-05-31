from flask import request, jsonify
from flask_smorest import Blueprint, abort as smorest_abort
from flask_jwt_extended import jwt_required, get_jwt_identity
from modelos.favorito_model import Favorito
from schemas.simple.post_simple_schema import PostSimpleSchema
from schemas.favorito_schema import FavoritoSchema
from modelos.post_model import Post
from extensions import db
from http import HTTPStatus
from flask.views import MethodView


favorito_bp = Blueprint('favoritos', __name__, description='Operaciones con Favoritos')


# ------------------- CRUD de Favoritos --------------------------#
@favorito_bp.route('/favoritos')
class FavoritoResource(MethodView):
    
    @favorito_bp.response(HTTPStatus.OK, FavoritoSchema(many=True))
    #@jwt_required()
    def get(self):
      """ Consultar todos los Favoritos"""
      id_usuario = get_jwt_identity()
      favoritos = Favorito.query.filter_by(id_usuario=id_usuario).all()
      if not favoritos:
          smorest_abort(HTTPStatus.NOT_FOUND, message="Aun no tiene Posts marcados como favorito")

      posts = [fav.post for fav in favoritos]

      return posts      

    @favorito_bp.arguments(FavoritoSchema)          
    @favorito_bp.response(HTTPStatus.CREATED, FavoritoSchema)
    #@jwt_required()
    def get(self, favorito_data):
        """ Consultar para crear un nuevo favorito """
        # Verificar si ya estaba marcado como favorito
        if Favorito.query.filter_by(id_post=favorito_data['id_post']).first():
           smorest_abort(HTTPStatus.BAD_REQUEST, message="Este Post ya esta marcado como favorito")

        # Crear el nuevo favorito
        nuevo_favorito = Favorito(id_post=favorito_data.id_post)

        db.session.add(nuevo_favorito)
        db.session.commit()

        return nuevo_favorito



# ------------------- Endpoint para ver favoritos por su ID --------------------------#

@favorito_bp.route('favoritos/<string:id_usuario>')
class FavoritoResourceID(MethodView):

  @favorito_bp.arguments(FavoritoSchema)          
  @favorito_bp.response(HTTPStatus.OK, FavoritoSchema)
  #@jwt_required()
  def get(self, id_favorito):
    """ Consultar un Post favorito por su ID"""
    favorito = Favorito.query.filter_by(id_favorito=id_favorito).first()
    if not favorito:
      smorest_abort(HTTPStatus.NOT_FOUND, message="No existe un post favorito con ese ID")
    return favorito    





#------------------  Enpoint para marcar un post como favorito ----------------------#

@favorito_bp.route('/favorito', methods=['POST'])
#@jwt_required()
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

@favorito_bp.route('/eliminar/<string:id_post>', methods=['DELETE'])
#@jwt_required()
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


