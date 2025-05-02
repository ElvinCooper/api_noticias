from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from modelos.favorito_model import Favorito
from modelos.post_model import Post
from extensions import db
from http import HTTPStatus

favorito_bp = Blueprint('favoritos', __name__)



@favorito_bp.route('/', methods=['GET'])
@jwt_required()
def obtener_favoritos_usuario():
    """
    Devuelve todos los posts marcados como favoritos por el usuario autenticado
    """
    id_usuario = get_jwt_identity()
    favoritos = Favorito.query.filter_by(id_usuario=id_usuario).all()
    
    posts = [fav.post for fav in favoritos]  # accedemos a los objetos Post relacionados

    from schemas.post_schema import PostSchema  # asegúrate de tener un esquema para Post
    post_schema = PostSchema(many=True)
    
    return jsonify(post_schema.dump(posts)), HTTPStatus.OK



# ------------------- Endpoint para ver favoritos de otro usuario --------------------------#

@favorito_bp.route('/usuario/<string:id_usuario>', methods=['GET'])
def favoritos_por_usuario(id_usuario):
    """
    Ver favoritos de un usuario específico (público o autenticado)
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
    Marcar un post como favorito para el usuario autenticado
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
    Elimina un post de los favoritos del usuario autenticado
    """
    id_usuario = get_jwt_identity()
    
    favorito = Favorito.query.filter_by(id_usuario=id_usuario, id_post=id_post).first()
    if not favorito:
        return jsonify({"mensaje": "Este post no está en tus favoritos"}), HTTPStatus.NOT_FOUND

    db.session.delete(favorito)
    db.session.commit()

    return jsonify({"mensaje": "Post eliminado de tus favoritos"}), HTTPStatus.OK


