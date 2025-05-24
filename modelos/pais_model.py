from extensions import db
import uuid



class Pais(db.Model):
    __tablename__ = 'paises'

    id_pais = db.Column(db.String, primary_key=True, default= lambda: str(uuid.uuid4()))
    nombre_pais = db.Column(db.String(50), nullable=False)
    abrebiatura_pais = db.Column(db.String(3), unique=True, nullable=False)
    id_multimedia    = db.Column(db.String, db.ForeignKey('multimedia.id_multimedia', use_alter=True, name="fk_pais_multimedia"),)    
    posts            = db.relationship('Post', back_populates='pais', lazy=True)   # Relacion con el modelo Pais