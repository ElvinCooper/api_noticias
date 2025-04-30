from sqlalchemy.orm import relationship
from extensions import db
import uuid



class Rol(db.Model):
    __tablename__ = 'roles'
    id_rol = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    descripcion = db.Column(db.String(50), unique=True, nullable=False)
    usuarios = relationship('Usuario', back_populates='rol')