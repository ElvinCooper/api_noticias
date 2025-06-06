from flask_smorest import Blueprint, abort as smorest_abort
from http import HTTPStatus
from schemas.post_categoria_schema import PostCategoriaSchema
from schemas.Error_schemas import ErrorSchema
from modelos.post_categoria_model import PostCategoria
from flask_jwt_extended import jwt_required
from flask.views import MethodView
from extensions import db




post_cat_bp = Blueprint('postCategoria', __name__, description='Operaciones con PostCategoria')

# ----------------------------  Consultar un post_categoria por su ID  --------------------------------#
@post_cat_bp.route('/postcat/<string:id_post>')
class ResourcePostCat(MethodView):

  @post_cat_bp.response(HTTPStatus.OK, PostCategoriaSchema(many=True))
  @post_cat_bp.alt_response(HTTPStatus.NOT_FOUND, schema=ErrorSchema, description="No existe un recurso con este id", example={"success": False, "message": "Not Found"})
  @post_cat_bp.alt_response(HTTPStatus.UNAUTHORIZED, schema=ErrorSchema, description="No autorizado", example={"success": False, "message": "No autorizado"})
  @post_cat_bp.alt_response(HTTPStatus.INTERNAL_SERVER_ERROR, schema=ErrorSchema, description="Error interno del servidor", example={"success": False, "message": "Error interno del servidor"})
  @jwt_required()
  def get(self, id_post):
    """ Consultar una pareja Post-Categoria por su ID"""
    postcats = db.session.get(PostCategoria, id_post)
    if not postcats:
      smorest_abort(HTTPStatus.NOT_FOUND, message="No existe ninguna categoria asociada a ese Post")

    return postcats  

