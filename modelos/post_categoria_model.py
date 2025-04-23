from extensions import db
import uuid


class PostCategoria(db.Model):
    __tablename__ = 'posts_categorias'
    
    id_post = db.Column(db.String, db.ForeignKey('posts.id_post', ondelete='CASCADE'), primary_key=True, default=lambda: str(uuid.uuid4()))
    id_categoria = db.Column(db.String, db.ForeignKey('categorias.id_categoria', ondelete='CASCADE'), primary_key=True, default=lambda: str(uuid.uuid4()))