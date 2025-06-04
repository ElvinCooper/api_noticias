from flask_smorest import Blueprint, abort as smorest_abort
from extensions import db
from http import HTTPStatus
from modelos.multimedia_model import Multimedia
from marshmallow.exceptions import ValidationError
from schemas.multimedia_schema import MultimediaSchema
from schemas.Error_schemas import ErrorSchema
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


    
    
    
    @multimedia_bp.arguments(MultimediaSchema)
    @multimedia_bp.response(201, MultimediaSchema)
    #@jwt_required()
    def post(self, data):
        """ Registrar un nuevo medio """
        # Verificar si ya existe uno con el mismo nombre
        if Multimedia.query.filter_by(nombre_archivo=data.nombre_archivo).first():
            smorest_abort(400, message="Ya existe un archivo con ese nombre.")
    

        nuevo_multimedia = Multimedia(**data)
        db.session.add(nuevo_multimedia)
        db.session.commit()

        return nuevo_multimedia
        

#--------------------- Endpoint para consultar un recurso multimedia por su id ----------------------#
@multimedia_bp.route('/multimedia/<string:id_multimedia>')
class MultimediaResourceID(MethodView):

    @multimedia_bp.arguments(MultimediaSchema)
    @multimedia_bp.response(HTTPStatus.OK, MultimediaSchema)
    @multimedia_bp.alt_response(HTTPStatus.NOT_FOUND, schema=ErrorSchema, description="No existe un recurso con este id", example={"success": False, "message": "Not Found"})
    @multimedia_bp.alt_response(HTTPStatus.UNAUTHORIZED, schema=ErrorSchema, description="No autorizado", example={"success": False, "message": "No autorizado"})
    @multimedia_bp.alt_response(HTTPStatus.INTERNAL_SERVER_ERROR, schema=ErrorSchema, description="Error interno del servidor", example={"success": False, "message": "Error interno del servidor"})
    #@jwt_required()    \comentado para pruebas
    def get(self, id_multimedia):
        """ Consultar un recurso por su ID """
        multimedia = Multimedia.query.filter_by(id_multimedia=id_multimedia).first()
        if not multimedia:
            smorest_abort(HTTPStatus.NOT_FOUND, message="Recurso no encontrado")
        return multimedia



