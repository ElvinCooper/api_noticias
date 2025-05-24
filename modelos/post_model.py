from extensions import db
from datetime import datetime, timezone
import uuid



class Post(db.Model):
    __tablename__ = 'posts'

    id_post    = db.Column(db.String, primary_key=True, default= lambda: str(uuid.uuid4()))
    titulo     = db.Column(db.String(100), nullable=False)
    contenido  = db.Column(db.String, nullable=False)
    id_usuario = db.Column(db.String(36), db.ForeignKey('usuarios.id_usuario', ondelete='CASCADE'), nullable=False)
    id_pais    = db.Column(db.String, db.ForeignKey('paises.id_pais', ondelete='RESTRICT'), nullable=False, default= lambda: str(uuid.uuid4()))
    fecha_publicacion = db.Column(db.DateTime, default=datetime.now(timezone.utc))
    visible     = db.Column(db.Boolean, default=True)
    autor       = db.relationship('Usuario', back_populates='posts')
    pais        = db.relationship('Pais', back_populates='posts', lazy=True)   # Relacion con el modelo Pais(posts)
    
    favoritos   = db.relationship('Favorito', back_populates='post', cascade='all, delete-orphan', passive_deletes=True)
    status     =  db.Column(db.Boolean, default=True)

    __table_args__ = (db.Index('idx_fecha_publicacion', 'fecha_publicacion'),)