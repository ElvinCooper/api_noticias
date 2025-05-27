from flask import request, jsonify
from flask_smorest import Blueprint, abort
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


#---------------- CRUD de Paises -------------------#

@pais_bp.route("/paises")
class PaisResource(MethodView):

    @pais_bp.response(HTTPStatus.OK, PaisSchema(many=True))
    # @jwt_required()
    def get(self):
        """ Consultar todos los paises en el sistema"""
        pais = Pais.query.all()                    
        return pais
    
    
    @pais_bp.arguments(PaisSchema)
    @pais_bp.response(HTTPStatus.CREATED, PaisSchema)
    #jwt_required()
    def post(self, pais_data):
        """ Registrar un nuevo Pais """
        # verfificar si ya existe un pais con esa descripcion
        if Pais.query.filter_by(nombre_pais=pais_data.nombre_pais):
            abort(HTTPStatus.BAD_REQUEST, message="Ya existe un pais con ese nombre")

        db.session.add(pais_data)    
        db.session.commit()
        return pais_data



# ----------------------------  Consultar una pais por su ID  --------------------------------#
@pais_bp.route("/pais/<string:id_pais>")
class PaisResourceId(MethodView):

    @pais_bp.response(HTTPStatus.OK, PaisSchema)
    @pais_bp.alt_response(HTTPStatus.NOT_FOUND, description='No existe un pais con ese ID')
    # @jwt_required()
    def get(self, id_pais):
        """ Consultar un Pais por su ID"""
        pais = Pais.query.filter_by(id_pais=id_pais).first()
        if not pais:
            abort(HTTPStatus.NOT_FOUND, message="País no encontrado.")
        return pais


