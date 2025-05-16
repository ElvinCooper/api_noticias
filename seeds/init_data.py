from modelos.categoria_model import Categoria
from modelos.rol_model import Rol
from modelos.pais_model import Pais
from extensions import db
import uuid

def seed_categorias():
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

    for nombre in categorias:
        if not Categoria.query.filter_by(descripcion=nombre).first():
            nueva = Categoria(id_categoria=str(uuid.uuid4()), descripcion=nombre)
            db.session.add(nueva)

    db.session.commit()


def seed_roles():
    roles = ['Administrador', 'Editor', 'Lector']
    for rol in roles:
        if not Rol.query.filter_by(descripcion=rol).first():
            nuevo = Rol(id_rol=str(uuid.uuid4()), descripcion=rol)
            db.session.add(nuevo)

    db.session.commit() 



def seed_paises():
    paises = [
        {"id_pais": "1", "nombre_pais": "Estados Unidos", "abrebiatura_pais": "USA"},
        {"id_pais": "44", "nombre_pais": "Reino Unido", "abrebiatura_pais": "GBR"},
        {"id_pais": "33", "nombre_pais": "Francia", "abrebiatura_pais": "FRA"},
        {"id_pais": "49", "nombre_pais": "Alemania", "abrebiatura_pais": "DEU"},
        {"id_pais": "34", "nombre_pais": "España", "abrebiatura_pais": "ESP"},
        {"id_pais": "39", "nombre_pais": "Italia", "abrebiatura_pais": "ITA"},
        {"id_pais": "809", "nombre_pais": "República Dominicana", "abrebiatura_pais": "DOM"},
        {"id_pais": "849", "nombre_pais": "República Dominicana", "abrebiatura_pais": "DOM"},
        {"id_pais": "52", "nombre_pais": "México", "abrebiatura_pais": "MEX"},
        {"id_pais": "55", "nombre_pais": "Brasil", "abrebiatura_pais": "BRA"},
        {"id_pais": "54", "nombre_pais": "Argentina", "abrebiatura_pais": "ARG"},
        {"id_pais": "56", "nombre_pais": "Chile", "abrebiatura_pais": "CHL"},
        {"id_pais": "57", "nombre_pais": "Colombia", "abrebiatura_pais": "COL"},
        {"id_pais": "51", "nombre_pais": "Perú", "abrebiatura_pais": "PER"},
        {"id_pais": "58", "nombre_pais": "Venezuela", "abrebiatura_pais": "VEN"},
        {"id_pais": "787", "nombre_pais": "Puerto Rico", "abrebiatura_pais": "PRI"},
        {"id_pais": "61", "nombre_pais": "Australia", "abrebiatura_pais": "AUS"},
        {"id_pais": "32", "nombre_pais": "Bélgica", "abrebiatura_pais": "BEL"},
        {"id_pais": "31", "nombre_pais": "Países Bajos", "abrebiatura_pais": "NLD"},
        {"id_pais": "41", "nombre_pais": "Suiza", "abrebiatura_pais": "CHE"},
        {"id_pais": "46", "nombre_pais": "Suecia", "abrebiatura_pais": "SWE"},
        {"id_pais": "47", "nombre_pais": "Noruega", "abrebiatura_pais": "NOR"},
        {"id_pais": "351", "nombre_pais": "Portugal", "abrebiatura_pais": "PRT"},
        {"id_pais": "353", "nombre_pais": "Irlanda", "abrebiatura_pais": "IRL"},
        {"id_pais": "416", "nombre_pais": "Canadá", "abrebiatura_pais": "CAN"},
    ]


    for pais_data in paises:
        # Verificar si el país ya existe por id_pais
        existe = Pais.query.filter_by(id_pais=pais_data["id_pais"]).first()
        if not existe:
            nuevo_pais = Pais(
                id_pais=pais_data["id_pais"],
                nombre_pais=pais_data["nombre_pais"],
                abrebiatura_pais=pais_data["abrebiatura_pais"],
                id_multimedia=None  # Dejamos NULL
            )
            db.session.add(nuevo_pais)

        db.session.commit()
        print(f"{len([p for p in paises if not Pais.query.filter_by(id_pais=p['id_pais']).first()])} países insertados (sin duplicados).")