from extensions import db
import uuid

class Multimedia(db.Model):
    __tablename__ = 'multimedia'

    id_multimedia = db.Column(db.String, primary_key=True, default=lambda: str(uuid.uuid4()))
    nombre_archivo = db.Column(db.String(50))
    url_multimedia_alt = db.Column(db.String(150))
    tipo_archivo   = db.Column(db.String(20), nullable=False)
   