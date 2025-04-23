from extensions import db
from datetime import datetime, timezone
import uuid

class Categoria(db.Model):
    __tablename__ = 'categorias'
    id_categoria = db.Column(db.String, primary_key=True, default=lambda: str(uuid.uuid4()))
    descripcion = db.Column(db.String(50), nullable=False)
    posts = db.relationship('Post', secondary='posts_categorias', back_populates='categorias')