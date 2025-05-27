from flask import request, jsonify, abort
from flask_smorest import Blueprint
from extensions import db
from http import HTTPStatus
from modelos.pais_model import Pais
from marshmallow.exceptions import ValidationError
from schemas.pais_schema import PaisSchema
from flask_jwt_extended import jwt_required
from flask.views import MethodView


pais_bp = Blueprint('pais', __name__, description='Operaciones con Pais')

pais_schema = PaisSchema()
paises_schema = PaisSchema(many=True)


#---------------- Endpoint para consultar todos los paises en la BD -------------------#
@pais_bp.route("/api/pais")
class PaisResource(MethodView):
    @pais_bp.response(HTTPStatus.OK, PaisSchema)
    # @jwt_required()
    def get(self):
        pais = Pais.query.all()                    
        return pais


# ----------------------------  Consultar una pais por su ID  --------------------------------#
@pais_bp.route("/api/pais/<string:id_pais>")
class PaisResourceId(MethodView):
    @pais_bp.response(HTTPStatus.OK, PaisSchema)
    # @jwt_required()
    def get(self, id_pais):
        pais = Pais.query.filter_by(id_pais=id_pais).first()
        if not pais:
            abort(HTTPStatus.NOT_FOUND, message="País no encontrado.")
        return pais



#----------------- Endpoint para registrar un nuevo pais en el sistema --------------------------#
from schemas.pais_schema import PaisCreateSchema
@pais_bp.route("/api/pais")
class PaisList(MethodView):
    @pais_bp.arguments(PaisCreateSchema)
    @pais_bp.response(HTTPStatus.CREATED, PaisSchema)
    # @jwt_required()  
    def post(self, pais_data):
        # Validar duplicado por ID
        if Pais.query.filter_by(id_pais=pais_data["id_pais"]).first():
            abort(HTTPStatus.BAD_REQUEST, message="Ya existe un país con ese ID.")

        nuevo_pais = Pais(id_pais=pais_data['id_pais'],
                          nombre_pais=pais_data['nombre_pais'],
                          abrebiatura_pais=pais_data['abrebiatura_pais'])

        db.session.add(nuevo_pais)
        db.session.commit()

        return nuevo_pais