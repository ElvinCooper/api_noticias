from marshmallow import fields, post_load, validate
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from modelos.multimedia_model import Multimedia


class MultimediaSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Multimedia
        load_instance = True
        #include_relationships = True
       

    id_multimedia  = fields.Str(dump_only=True)  # UUID como string
    nombre_archivo = fields.Str(allow_none=True, validate=validate.Length(50))
    url_multimedia_alt = fields.Str(allow_none=True)
    tipo_archivo   = fields.Str(required=True,   validate=validate.Length(20))
    
    
    @post_load
    def make_multimedia(self, data, **kwargs):
        return Multimedia(
            nombre_archivo=data.get('nombre_archivo'),
            tipo_entidad=data.get('tipo_entidad'),
            tipo_archivo=data['tipo_archivo']
        )
