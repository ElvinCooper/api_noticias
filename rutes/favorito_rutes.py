from flask_smorest import Blueprint, abort as smorest_abort
from flask_jwt_extended import jwt_required, get_jwt_identity
from modelos.favorito_model import Favorito
from schemas.favorito_schema import FavoritoSchema
from schemas.Error_schemas import ErrorSchema
from modelos.post_model import Post
from extensions import db
from http import HTTPStatus
from flask.views import MethodView


favorito_bp = Blueprint('favoritos', __name__, description='Operaciones con Favoritos')


# ------------------- CRUD de Favoritos --------------------------#
@favorito_bp.route('/favoritos')
class FavoritoResource(MethodView):
    
    @favorito_bp.response(HTTPStatus.OK, FavoritoSchema(many=True))
    @jwt_required()
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
    @favorito_bp.alt_response(HTTPStatus.BAD_REQUEST, schema=ErrorSchema, description="Falta el campo id_post", example={"success": False, "message": "El campo 'id_post' es obligatorio"})
    @favorito_bp.alt_response(HTTPStatus.INTERNAL_SERVER_ERROR, schema=ErrorSchema, description="Error interno del servidor", example={"success": False, "message": "Error interno del servidor"})
    
    @jwt_required()
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
  @favorito_bp.alt_response(HTTPStatus.INTERNAL_SERVER_ERROR, schema=ErrorSchema, description="Error interno del servidor", example={"success": False, "message": "Error interno del servidor"})
  @jwt_required()
  def get(self, id_favorito):
    """ Consultar un Post favorito por su ID"""
    favorito = Favorito.query.filter_by(id_favorito=id_favorito).first()
    if not favorito:
      smorest_abort(HTTPStatus.NOT_FOUND, message="No existe un post favorito con ese ID")
    return favorito    





#------------------  Enpoint para marcar un post como favorito ----------------------#

from schemas.favorito_schema import FavoritoInputSchema, FavoritoResponseSchema

@favorito_bp.route("/favorito/crear")
class MarcarFavoritoResource(MethodView):

    @jwt_required()
    @favorito_bp.arguments(FavoritoInputSchema)
    @favorito_bp.response(HTTPStatus.CREATED, FavoritoResponseSchema)
    @favorito_bp.alt_response(HTTPStatus.BAD_REQUEST, schema=ErrorSchema, description="Falta el campo id_post", example={"success": False, "message": "El campo 'id_post' es obligatorio"})
    @favorito_bp.alt_response(HTTPStatus.NOT_FOUND, schema=ErrorSchema, description="Post no encontrado", example={"success": False, "message": "El post no existe"})
    @favorito_bp.alt_response(HTTPStatus.CONFLICT, schema=ErrorSchema, description="Ya marcado como favorito", example={"success": False, "message": "Este post ya está en tus favoritos"})
    def post(self, data):
        """Marcar un post como favorito"""
        id_post = data.get("id_post")
        id_usuario = get_jwt_identity()

        post = Post.query.get(id_post)
        if not post:
            smorest_abort(HTTPStatus.NOT_FOUND, message="El post no existe")

        favorito_existente = Favorito.query.filter_by(id_usuario=id_usuario, id_post=id_post).first()
        if favorito_existente:
            smorest_abort(HTTPStatus.CONFLICT, message="Este post ya está en tus favoritos")

        nuevo_favorito = Favorito(id_usuario=id_usuario, id_post=id_post)
        db.session.add(nuevo_favorito)
        db.session.commit()

        return {
            "mensaje": "Post agregado a favoritos exitosamente",
            "id_usuario": id_usuario,
            "id_post": id_post
        }



#------------------------------------ Enpoint para eliminar un favorito ---------------------------------------#
from schemas.favorito_schema import FavoritoDeleteSchema
@favorito_bp.route("/favorito/eliminar")
class DeleteFavoritoResource(MethodView):

    @jwt_required()
    @favorito_bp.arguments(FavoritoDeleteSchema)
    @favorito_bp.response(HTTPStatus.OK, FavoritoDeleteSchema)
    @favorito_bp.alt_response(HTTPStatus.BAD_REQUEST, schema=ErrorSchema, description="Falta el campo id_post", example={"success": False, "message": "El campo 'id_post' es obligatorio"})
    @favorito_bp.alt_response(HTTPStatus.NOT_FOUND, schema=ErrorSchema, description="Post no encontrado", example={"success": False, "message": "El post no existe"})
    def delete(self, data):
        """Eliminar un post como favorito"""
        id_post = data.get("id_post")
        id_usuario = get_jwt_identity()
    
        favorito = Favorito.query.filter_by(id_usuario=id_usuario, id_post=id_post).first()
        if not favorito:
            smorest_abort(HTTPStatus.NOT_FOUND, message="Este post no está en tus favoritos")

        db.session.delete(favorito)
        db.session.commit()

        return {"success": True, "message": "Favorito eliminado de tus favoritos"}, HTTPStatus.OK

