from flask import request, jsonify, abort
from flask_smorest import Blueprint
from extensions import db
from http import HTTPStatus
from modelos.multimedia_model import Multimedia
from marshmallow.exceptions import ValidationError
from schemas.pais_schema import MultimediaSchema
from flask_jwt_extended import jwt_required
from flask.views import MethodView

multimedia_bp = Blueprint('multimedia', __name__, description='Operaciones con Multimedia')

multimedia_schema   = MultimediaSchema()
multimedias_schemas = MultimediaSchema(many=True)



#--------------------- Endpoint para obtener todos los datos multimedias del sistema ----------------------#
@multimedia_bp.get('/multimedia')
class MultimediaResource(MethodView):

    @multimedia_bp.response(HTTPStatus.OK, MultimediaSchema(many=True))
    #@jwt_required()
    def get(self):    
        """ Consultar todos los elementos multimedia"""
        multimedia = Multimedia.query.all()
        return multimedia


    @multimedia_bp.route("/multimedia")
    class MultimediaList(MethodView):
        #@jwt_required()
        @multimedia_bp.arguments(MultimediaSchema)
        @multimedia_bp.response(201, MultimediaSchema)
        def post(self, data):
            """ Registrar un nuevo medio """
            # Verificar si ya existe uno con el mismo nombre
            if Multimedia.query.filter_by(nombre_archivo=data.nombre_archivo).first():
                abort(400, message="Ya existe un archivo con ese nombre.")
        

            db.session.add(data)
            db.session.commit()
            return data
        

#--------------------- Endpoint para consultar un recurso multimedia por su id ----------------------#
@multimedia_bp.route('/multimedia/<string:id_multimedia>')
class MultimediaResourceID(MethodView):

    @multimedia_bp.arguments(MultimediaSchema)
    @multimedia_bp.response(HTTPStatus.OK, MultimediaSchema)
    #@jwt_required()    \comentado para pruebas
    def get(self, id_multimedia):
        """ Consultar un recurso por su ID """
        multimedia = Multimedia.query.filter_by(id_multimedia=id_multimedia).first()
        if not multimedia:
            abort(HTTPStatus.NOT_FOUND, mesage="Recurso no encontrado")
        return multimedia



