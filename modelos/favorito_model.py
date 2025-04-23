from extensions import db
import uuid


class Favorito(db.Model):
    __tablename__ = 'favoritos'

    id_usuario = db.Column(db.String, db.ForeignKey('usuarios.id_usuario', ondelete='CASCADE'), primary_key=True, default=lambda: str(uuid.uuid4()))
    id_post = db.Column(db.String, db.ForeignKey('posts.id_post', ondelete='CASCADE'), primary_key=True)
    usuario = db.relationship('Usuario', back_populates='favoritos')
    post = db.relationship('Post', back_populates='favoritos')