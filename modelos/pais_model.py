from extensions import db
from datetime import datetime, timezone
import uuid



class Pais(db.Model):
    __tablename__ = 'paises'
    id_pais = db.Column(db.String, primary_key=True, default= lambda: str(uuid.uuid4()))
    descripcion = db.Column(db.String(50), nullable=False)
    codigo_iso = db.Column(db.String(3), unique=True, nullable=False)
    posts = db.relationship('Post', back_populates='pais')