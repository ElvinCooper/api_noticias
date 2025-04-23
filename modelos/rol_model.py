#from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, ForeignKey, Index
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from extensions import db
import uuid



class Rol(db.Model):
    __tablename__ = 'roles'
    id_rol = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    descripcion = db.Column(db.String(50), unique=True, nullable=False)
    usuarios = relationship('Usuario', back_populates='rol')