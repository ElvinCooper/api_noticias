from flask import Blueprint, request, jsonify
from extensions import db
from http import HTTPStatus
from modelos.pais_model import Pais
from marshmallow.exceptions import ValidationError
from schemas.pais_schema import PaisSchema
from flask_jwt_extended import jwt_required


pais_bp = Blueprint('pais', __name__)

pais_schema = PaisSchema()
paises_schema = PaisSchema(many=True)


#---------------- Endpoint para consultar todos los paises en la BD -------------------#
@pais_bp.route('/paises', methods=['GET'])
#@jwt_required()
def consultar_paises():
    """
    Consultar todos los paises.

    Este endpoint retorna la lista de todos los paises registrados en el sistema.
    ---
    tags:
      - Paises    
    responses:
      200:
        description: Lista de paises
        schema:
           $ref: '#/definitions/Paises'
    """    
    paises = Pais.query.all()
    return jsonify(paises_schema.dump(paises)), HTTPStatus.OK




# ----------------------------  Consultar una pais por su ID  --------------------------------#
@pais_bp.route('/paises/<string:id_pais>', methods=['GET'])
#@jwt_required()
def obtener_pais_por_id(id_pais):
    """
    Consultar un pais por su ID.

    Este endpoint retorna el pais registrado con el id proporcionado.
    ---
    tags:
      - Paises
    parameters:
      - name: id_pais
        in: path
        type: string
        required: true
        description: ID del pais  
    responses:
      200:
        description: Pais filtrado
        schema:
           $ref: '#/definitions/Paises'
    """
    pais = Pais.query.filter_by(id_pais=id_pais).first()
    if not pais:
        return jsonify({"error": "Pais no encontrado"}), HTTPStatus.NOT_FOUND
    
    return jsonify(pais_schema.dump(pais)), HTTPStatus.OK    