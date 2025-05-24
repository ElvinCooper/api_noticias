from flask import Blueprint, request, jsonify
from extensions import db
from http import HTTPStatus
from modelos.multimedia_model import Multimedia
from marshmallow.exceptions import ValidationError
from schemas.pais_schema import MultimediaSchema
from flask_jwt_extended import jwt_required

multimedia_bp = Blueprint('multimedia', __name__)

multimedia_schema   = MultimediaSchema()
multimedias_schemas = MultimediaSchema(many=True)



#--------------------- Endpoint para obtener todos los datos multimedias del sistema ----------------------#
@multimedia_bp.get('/')
#@jwt_required()
def get_todos():    
    """
    Consultar todos los registros de multimedia.

    Este endpoint retorna la lista de todos los datos de multimedia registrados en el sistema.
    ---
    tags:
        - Multimedia
    responses:
        200:
          description: Lista de multimedias
          schema:
            type: array
            items:
                $ref: '#/definitions/Multimedia'
    """    

    multimedia = Multimedia.query.all()
    return jsonify(multimedias_schemas.dump(multimedia)), HTTPStatus.OK




#--------------------- Endpoint para consultar un recurso multimedia por su id ----------------------#
@multimedia_bp.get('/<string:id_multimedia>')
#@jwt_required()    \comentado para pruebas
def get_one(id_multimedia):
    """
    Consultar un registro multimedia por su id.

    Este endpoint retorna un registro multimedia registrado en el sistema por su id.
    ---
    tags:
        - Multimedia
    parameters:
      - name: id_multimedia
        in: path
        type: string
        required: true
        description: ID del registro multimedia
    responses:
        200:
          description: Recurso multimedia
          schema:            
            $ref: '#/definitions/Multimedia'
        404:
          description: No existe un recurso con ese id    
    """ 

    # veificar si existe el recurso por el id
    multimedia = Multimedia.query.filter_by(id_multimedia=id_multimedia).first()
    if not multimedia:
        return jsonify({"mensaje": "No existe un recurso con ese id"})
    
    return jsonify(multimedia_schema.dump(multimedia)), HTTPStatus.OK
