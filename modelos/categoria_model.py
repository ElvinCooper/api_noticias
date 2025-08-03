from extensions import db
import uuid

class Categoria(db.Model):
    __tablename__ = 'categorias'

    id_categoria = db.Column(db.String, primary_key=True, default=lambda: str(uuid.uuid4()))
    descripcion = db.Column(db.String(50), nullable=False)
    eslogan_cat     = db.Column(db.String(100))
    id_multimedia = db.Column(db.String, db.ForeignKey('multimedia.id_multimedia'), nullable=True)
    post = db.relationship('Post', back_populates='categoria', lazy=True)