from extensions import db
import uuid

class Multimedia(db.Model):
    __tablename__ = 'multimedia'
    id_multimedia = db.Column(db.Integer, primary_key=True, default=lambda: str(uuid.uuid4()))
    id_post = db.Column(db.Integer, db.ForeignKey('posts.id_post', ondelete='CASCADE'), nullable=False)
    url = db.Column(db.String, nullable=False)
    tipo = db.Column(db.String(20), nullable=False)
    descripcion = db.Column(db.String)
    post = db.relationship('Post', back_populates='multimedia')