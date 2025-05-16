from extensions import db
import uuid

class Multimedia(db.Model):
    __tablename__ = 'multimedia'

    id_multimedia = db.Column(db.String, primary_key=True, default=lambda: str(uuid.uuid4()))
    id_post = db.Column(db.String, db.ForeignKey('posts.id_post', use_alter=True, name="fk_multimedia_post"), nullable=False)
    nombre_archivo = db.Column(db.String(50))
    tipo_entidad   = db.Column(db.String(20))
    tipo_archivo   = db.Column(db.String(20), nullable=False)
    categoria      = db.relationship('Categoria', back_populates='multimedia', uselist=False)  # Relacion uno a uno
    pais           = db.relationship('Pais', back_populates='multimedia', uselist=False) # relacion uno a uno
    post           = db.relationship('Post', back_populates='multimedia', lazy=True)