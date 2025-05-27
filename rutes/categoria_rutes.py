from flask import request, jsonify, abort
from flask_smorest import Blueprint
from flask.views import MethodView
from extensions import db
from http import HTTPStatus
from marshmallow.exceptions import ValidationError
from datetime import timedelta
from schemas.categoria_schema import CategoriaSchema
from modelos.categoria_model import Categoria
from flask_jwt_extended import jwt_required


categorias_bp = Blueprint('categorias', __name__, description="Operaciones con Categorias")
categoria_schema = CategoriaSchema()
categorias_schemas = CategoriaSchema(many=True)


# ----------------------------  Consultar todas las categorias  --------------------------------#
@categorias_bp.route("/api/categoria")
class CategoriaResource(MethodView):
    @categorias_bp.response(HTTPStatus.OK, CategoriaSchema)
    # @jwt_required()
    def get(self):
        categoria = Categoria.query.all()        
        return categoria


# ----------------------------  Consultar una categoria por su ID  --------------------------------#
@categorias_bp.route('/categoria/<string:id_categoria>')
class CategoriaResourceId(MethodView):
  @categorias_bp.response(HTTPStatus.OK, CategoriaSchema)  
  #@jwt_required()
  def get(self, id_categoria):
      categoria = Categoria.query.filter_by(id_categoria=id_categoria).first()
      if not categoria:
          abort(HTTPStatus.NOT_FOUND, message="Categoria no encontrada")


# ----------------------------  Registar una nueva categoria  --------------------------------#
from flask.views import MethodView

@categorias_bp.route("/api/categoria")
class CategoriaList(MethodView):
    @categorias_bp.arguments(CategoriaSchema)
    @categorias_bp.response(201, CategoriaSchema)
    # @jwt_required()  
    def post(self, categoria_data):
        if Categoria.query.filter_by(descripcion=categoria_data.descripcion).first():
            abort(400, message="Ya existe una categoría con esa descripción.")

        db.session.add(categoria_data)
        db.session.commit()

        return categoria_data