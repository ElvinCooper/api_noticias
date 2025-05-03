from extensions import db


posts_categorias = db.Table('posts_categorias',
    db.Column('id_post', db.String, db.ForeignKey('posts.id_post'), primary_key=True),
    db.Column('id_categoria', db.String, db.ForeignKey('categorias.id_categoria'), primary_key=True)
)


