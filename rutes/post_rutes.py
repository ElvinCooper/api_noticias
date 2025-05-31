from flask import request, jsonify
from flask_smorest import Blueprint, abort as smorest_abort
from modelos.post_model import Post
from modelos.post_categoria_model import PostCategoria
from modelos.categoria_model import Categoria
from modelos.user_model import Usuario
from schemas.post_schema import PostSchema
from flask_jwt_extended import jwt_required, get_jwt_identity
from extensions import db
from http import HTTPStatus
from modelos.pais_model import Pais
from marshmallow.exceptions import ValidationError
from flask.views import MethodView



post_bp = Blueprint('post', __name__, description='Operaciones con Post')


#---------------------- CRUD de los Posts con paginacion --------------------------#
from schemas.post_schema import PaginationSchema, PaginatedPostsSchema
@post_bp.route('/posts')
class PostResource(MethodView):
   
   @post_bp.arguments(PaginationSchema, location="query", as_kwargs=True)
   @post_bp.response(HTTPStatus.OK, PaginatedPostsSchema)
   #@jwt_required() 
   def get(self, page=1, per_page=10):
    """ Consultar todos los Posts"""
    pagination = Post.query.paginate(
       page=page,
       per_page=per_page,
       error_out=False
    )

    #posts = Post.query.all()
    return {
       'posts': pagination.items,
       'total': pagination.total,
       'pages': pagination.pages,
       'current_page': pagination.page,
       'per_page': pagination.per_page,
       'has_next': pagination.has_next,
       'has_prev': pagination.has_prev
    }
   

   @post_bp.arguments(PostSchema)
   @post_bp.response(HTTPStatus.CREATED, PostSchema)
   #jwt_required()
   def post(self, post_data):
      """ Crear un nuevo Post"""

      try:
          # validar la existencia del pais
          pais = Pais.query.filter_by(id_pais=post_data.id_pais).first()  #validar si el codigo de pais recibido existe

          # Obtener y validar categorías (si existen)
          categorias_ids = getattr(post_data, 'categorias', []) or []
          categorias_validas = [] 
          
          # Validar la existencia del pais
          if not pais:
            smorest_abort(HTTPStatus.NOT_FOUND, message="No existe un pais con ese ID")           


          # Validar existencia del usuario          
          usuario = db.session.get(Usuario, post_data.id_usuario )
          if not usuario:
             smorest_abort(HTTPStatus.NOT_FOUND, message="No existe un usuario con ese ID")

          for id_categoria in categorias_ids:
                categoria = Categoria.query.get(id_categoria)
                if categoria:
                    categorias_validas.append(id_categoria)   


          # Llenar la tabla de PostCategoria
          for id_categoria in categorias_validas:
             relacion = PostCategoria(id_post=post_data.id_post, id_categoria=id_categoria)
             db.session.add(relacion)          

          
          # Crear el Post
          db.session.add(post_data)    
          db.session.flush()  # para obtener el ID del post antes del commit

          # Insertar relaciones
          for id_categoria in categorias_validas:
            relacion = PostCategoria(id_post=post_data.id_post, id_categoria=id_categoria)
            db.session.add(relacion)


          db.session.commit()  
          return post_data
      
      except Exception as e:
         db.session.rollback()
         smorest_abort(HTTPStatus.BAD_REQUEST, message=f"Error al crear post: {str(e)}")
      


#------------------------ Enpoint consultar un post con su ID ----------------------#
@post_bp.route('post/<string:id_post>')
class PostResourceID(MethodView):
   
   @post_bp.response(HTTPStatus.OK, PostSchema)
   #jwt_required()
   def get(self, id_post):
    """ Consultar un Post por su ID"""
       
    post = db.session.get(Post, id_post)
    if not post:
       smorest_abort(HTTPStatus.NOT_FOUND, message='No existe ninnug Post con ese ID')

    return post    



#------------------------ Actualizar o Editar  un Post -----------------------------#
from schemas.post_schema import PostUpdateSchema
@post_bp.route("/posts/<string:id_post>")
class PostItemResource(MethodView):
    @jwt_required()
    @post_bp.arguments(PostUpdateSchema)  
    @post_bp.response(HTTPStatus.OK, PostSchema)  
    def put(self, update_data, id_post):
      """ Actualizar un Post existente"""
      
      id_usuario = get_jwt_identity()
      post = db.session.get(Post, id_post)

      if not post:
        smorest_abort(HTTPStatus.NOT_FOUND, message="Post no encontrado")

        if post.id_usuario != id_usuario:
           abort(HTTPStatus.FORBIDDEN, message="No tienes permisos para editar este post")

        try:
            if update_data.get("id_pais"):
                post.id_pais = update_data["id_pais"]
            if update_data.get("titulo"):
                post.titulo = update_data["titulo"]
            if update_data.get("contenido"):
                post.contenido = update_data["contenido"]

            db.session.commit()
            return post

        except Exception as err:
            db.session.rollback()
            abort(HTTPStatus.BAD_REQUEST, message=f"Error al actualizar el post: {str(err)}")






# ------------------------ Endpoint para eliminar un Post ---------------------------- #
from schemas.post_schema import PostUpdateSchema
@post_bp.route("/posts/<string:id_post>")
class PostItemResource(MethodView):
    @jwt_required()
    @post_bp.arguments(PostUpdateSchema)  
    @post_bp.response(HTTPStatus.OK, PostSchema)  
    def put(self, update_data, id_post):
      """ Actualizar un Post existente"""
      
      id_usuario = get_jwt_identity()
      post = db.session.get(Post, id_post)

      if not post:
        smorest_abort(HTTPStatus.NOT_FOUND, message="Post no encontrado")

        if post.id_usuario != id_usuario:
           abort(HTTPStatus.FORBIDDEN, message="No tienes permisos para eliminar este post")

      try:
        db.session.delete(post)
        db.session.commit()
        return '', HTTPStatus.NO_CONTENT
      
      except Exception as err:
         db.session.rollback()
         smorest_abort(HTTPStatus.BAD_REQUEST, message=f"Error al eliminar el post: {str(err)}")



