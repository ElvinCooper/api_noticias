from extensions import db
import uuid

class Categoria(db.Model):
    __tablename__ = 'categorias'

    id_categoria = db.Column(db.String, primary_key=True, default=lambda: str(uuid.uuid4()))
    descripcion = db.Column(db.String(50), nullable=False)
    id_multimedia = db.Column(db.String, db.ForeignKey('multimedia.id_multimedia'), nullable=True)
    multimedia = db.relationship('Multimedia', back_populates='categoria') # Relacion uno a uno
    posts      = db.relationship('Post',secondary='posts_categorias', back_populates='categorias')  # Relacion con Post