from flask import Blueprint, request, jsonify
from extensions import db
from http import HTTPStatus
from marshmallow.exceptions import ValidationError
from datetime import timedelta
from schemas.categoria_schema import CategoriaSchema
from modelos.categoria_model import Categoria
from flask_jwt_extended import jwt_required



categorias_bp = Blueprint('categorias', __name__)
categoria_schema = CategoriaSchema()
categorias_schemas = CategoriaSchema(many=True)



# ----------------------------  Consultar todas las categorias  --------------------------------#
@categorias_bp.route('/categorias', methods=['GET'])
@jwt_required()
def obtener_categorias():
    """
    Obtener todas las categorías

    Este endpoint retorna la lista completa de categorías disponibles en el sistema, incluyendo su descripción e ID.
    ---
    tags:
      - Categorías
    responses:
      200:
        description: Lista de categorías
        schema:
          type: array
          items:
            $ref: '#/definitions/Categoria'
    """
    categoria = Categoria.query.all()
    return jsonify(categorias_schemas.dump(categoria)), HTTPStatus.OK
    


# ----------------------------  Consultar una categoria por su ID  --------------------------------#
@categorias_bp.route('/categoria/<string:id_categoria>', methods=['GET'])
@jwt_required()
def obtener_categoria_por_id(id_categoria):
    """
    Obtener una categoría por ID

    Este endpoint permite consultar los detalles de una categoría específica usando su ID.
    ---
    tags:
      - Categorías
    parameters:
      - name: id_categoria
        in: path
        type: string
        required: true
        description: ID de la categoría a consultar
    responses:
      200:
        description: Categoría encontrada
        schema:
          $ref: '#/definitions/Categoria'
      404:
        description: Categoría no encontrada
    """
    categoria = Categoria.query.get_or_404(id_categoria)

    if not categoria:
        return jsonify({"error": "Categoria no encontrada"}), HTTPStatus.NOT_FOUND
    
    return jsonify(categoria_schema.dump(categoria)), HTTPStatus.OK