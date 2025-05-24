from flask import request, jsonify
from flask_smorest import Blueprint
from extensions import db
from http import HTTPStatus
from modelos.pais_model import Pais
from marshmallow.exceptions import ValidationError
from schemas.pais_schema import PaisSchema
from flask_jwt_extended import jwt_required


pais_bp = Blueprint('pais', __name__, description='Operaciones con Pais')

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
      404:
        description: Pais no encontrado.      
    """
    pais = Pais.query.filter_by(id_pais=id_pais).first()
    if not pais:
        return jsonify({"error": "Pais no encontrado"}), HTTPStatus.NOT_FOUND
    
    return jsonify(pais_schema.dump(pais)), HTTPStatus.OK    



#----------------- Endpoint para registrar un nuevo pais en el sistema --------------------------#
@pais_bp.post('/crear')
#@jwt_required()
def registar_pais():
  """
  Registrar un nuevo Pais en el sistema.

  Este endpoint permiter registrar un nuevo pais indicando su codigo de area como id, nombre y abrebiatura de pais.
  ---
    tags:
      - Paises
    parameters:
      - name: body
        in: body
        required: true
        schema:
          $ref: '#/definitions/Paises' 
    responses:
      200:
        description: Pais registrado exitosamente.
        schema:
           $ref: '#/definitions/Paises'   
      400:
        description: faltan un o varios campos por en la solicitud, favor revisar.     
  """
  try:
    data = request.get_json()
    id_pais = data.get('id_pais')
    nombre = data.get('nombre')
    abrebiatura_pais = data.get('abrebiatura_pais')
    

    # verificar si existen todos los campos en la solicitud.
    if not all ([id_pais, nombre, abrebiatura_pais]):
      return jsonify({"mensaje": "faltan un o varios campos por en la solicitud, favor revisar"}), HTTPStatus.BAD_REQUEST
          
    # validar que el id_pais no se este en la base de datos
    if Pais.query.filter_by(id_pais=id_pais).first():
      return jsonify({"error": "Ya existe un pais con ese id"})
    
    # Creacion de la nueva categoria
    nuevo_pais = Pais(id_pais = id_pais,
                      nombre  = nombre,
                      abrebiatura_pais = abrebiatura_pais)
    
    db.session.add(nuevo_pais)
    db.session.commit()      

    return jsonify(pais_schema.dump(nuevo_pais)), HTTPStatus.CREATED        
  
  except ValidationError as err:
    return jsonify({"error": err.messages}), HTTPStatus.BAD_REQUEST