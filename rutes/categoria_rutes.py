from flask_smorest import Blueprint, abort
from flask.views import MethodView
from extensions import db
from http import HTTPStatus  
from marshmallow.exceptions import ValidationError
from schemas.categoria_schema import CategoriaSchema
from modelos.categoria_model import Categoria
from flask_jwt_extended import jwt_required
from schemas.Error_schemas import ErrorSchema
from modelos.post_categoria_model import PostCategoria


categorias_bp = Blueprint('categorias', __name__, description="Operaciones con Categorias")


# ----------------------------  CRUD Categorias  --------------------------------#
@categorias_bp.route("/categoria")
class CategoriaResource(MethodView):

    @categorias_bp.response(HTTPStatus.OK, CategoriaSchema(many=True))
    #@jwt_required()
    def get(self):
        """ Consultar todas la categorias con total de publicaciones"""
        categorias = Categoria.query.all() 

        for categoria in categorias:
            categoria.total_posts = db.session.query(PostCategoria).filter_by(id_categoria=categoria.id_categoria).count()

        return categorias


    @categorias_bp.arguments(CategoriaSchema)
    @categorias_bp.response(HTTPStatus.CREATED, CategoriaSchema)    
    @jwt_required()
    def post(self, categoria_data):
        """ Registrar una nueva Categoria"""
        # verificar si existe una categoria 
        if Categoria.query.filter_by(descripcion=categoria_data.descripcion).first():
            abort(HTTPStatus.BAD_REQUEST, message="Ya existe una catgoria con esa descripcion.")

        db.session.add(categoria_data)
        db.session.commit()
        return categoria_data
    

# ----------------------------  Consultar una categoria por su ID  --------------------------------#
@categorias_bp.route('/categoria/<string:id_categoria>')
class CategoriaResourceId(MethodView):
  
  @categorias_bp.response(HTTPStatus.OK, CategoriaSchema)  
  @categorias_bp.alt_response(HTTPStatus.NOT_FOUND, schema=ErrorSchema, description="No existe un recurso con este id", example={"success": False, "message": "Not Found"})
  @categorias_bp.alt_response(HTTPStatus.UNAUTHORIZED, schema=ErrorSchema, description="No autorizado", example={"success": False, "message": "No autorizado"})
  @categorias_bp.alt_response(HTTPStatus.INTERNAL_SERVER_ERROR, schema=ErrorSchema, description="Error interno del servidor", example={"success": False, "message": "Error interno del servidor"})
  @jwt_required()
  def get(self, id_categoria):
      """ Consultar una categoria por su ID"""
      categoria = Categoria.query.filter_by(id_categoria=id_categoria).first()
      if not categoria:
          abort(HTTPStatus.NOT_FOUND, message="Categoria no encontrada")
      return categoria    


