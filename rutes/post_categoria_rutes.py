from flask_smorest import Blueprint, abort as smorest_abort
from http import HTTPStatus
from schemas.post_categoria_schema import PostCategoriaSchema
from modelos.post_categoria_model import PostCategoria
from flask_jwt_extended import jwt_required
from flask.views import MethodView
from extensions import db



post_cat_bp = Blueprint('postCategoria', __name__, description='Operaciones con PostCategoria')








# ----------------------------  Consultar un post_categoria por su ID  --------------------------------#
@post_cat_bp.route('/postcat/<string:id_post>')
class ResourcePostCat(MethodView):

  @post_cat_bp.response(HTTPStatus.OK, PostCategoriaSchema(many=True))
  #@jwt_required()
  def get(self, id_post):
    """ Consultar una pareja Post-Categoria por su ID"""
    postcats = db.session.get(PostCategoria, id_post)
    if not postcats:
      smorest_abort(HTTPStatus.NOT_FOUND, message="No existe ninguna categoria asociada a ese Post")

    return postcats  

