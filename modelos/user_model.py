from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from extensions import db
import uuid

class Usuario(db.Model):
    __tablename__ = 'usuarios'
    
    id_usuario = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    nombre = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    id_rol = db.Column(db.String(36), db.ForeignKey('roles.id_rol', ondelete='RESTRICT'), nullable=False)
    fecha_registro = db.Column(db.Datetime, default=datetime.now(timezone.utc))
    rol = relationship('Rol', back_populates='usuarios')
    posts = relationship('Post', back_populates='autor')
    favoritos = relationship('Favorito', back_populates='usuario')

    __table_args__ = (db.Index('idx_email', 'email'),)