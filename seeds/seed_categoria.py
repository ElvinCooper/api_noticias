from app import app
from extensions import db
from modelos.categoria_model import Categoria
import uuid


def cargar_categorias():
    categorias = [
        'Última Hora', 'Nacionales', 'Internacionales', 'Política', 'Economía',
        'Negocios', 'Tecnología', 'Startups', 'Ciencia', 'Ciberseguridad',
        'IA / Machine Learning', 'Salud', 'Bienestar', 'Nutrición', 'Fitness',
        'Psicología', 'Cultura', 'Música', 'Cine / Series', 'Libros', 'Arte',
        'Fútbol', 'Baloncesto', 'Tenis', 'Otros Deportes', 'Medioambiente',
        'Cambio Climático', 'Educación', 'Derechos Humanos', 'Sociedad',
        'Opinión', 'Editorial', 'Análisis', 'Borradores',
        'Archivadas', 'Contenido Destacado', 'Tendencias'
    ]

    with app.app_context():
        for nombre in categorias:
            existe = Categoria.query.filter_by(descripcion=nombre).first()
            if not existe:
                nueva = Categoria(
                    id_categoria=str(uuid.uuid4()),
                    descripcion=nombre,
                    id_multimedia=None
                )
                db.session.add(nueva)

        db.session.commit()
        print(f" {len(categorias)} categorías insertadas (sin duplicados).")


if __name__ == "__main__":
    cargar_categorias()
