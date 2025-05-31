from marshmallow import fields, post_load, validate
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from modelos.multimedia_model import Multimedia
from extensions import db


class MultimediaSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Multimedia
        load_instance = True
        sqla_session = db.session
        schema_name= "MulimediaSchema"
       

    id_multimedia  = fields.Str(dump_only=True)  # UUID como string
    nombre_archivo = fields.Str(allow_none=True, validate=validate.Length(min=10, max=60))
    url_multimedia_alt = fields.Str(allow_none=True)
    tipo_archivo   = fields.Str(required=True,   validate=validate.Length(max=20))
    
    
   
