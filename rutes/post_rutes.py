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

# Esquemas para Serializacion/Deserializacion
post_schema   = PostSchema()
posts_schemas = PostSchema(many=True)


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
          usuario = Usuario.query.filter_by(id_usuario=post_data.id_usuario).first()
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
       
    post = Post.query.filter_by(id_post=id_post).first()
    if not post:
       smorest_abort(HTTPStatus.NOT_FOUND, message='No existe ninnug Post con ese ID')

    return post    



#------------------------ Actualizar o Editar  un Post -----------------------------#
@post_bp.route('/update/<string:id_post>', methods=['PUT'])
#@jwt_required()
def actualizar_post(id_post):
  """
    Actualizar Post

    Permite a un usuario autenticado editar un Post creado.
    ---
    tags:
      - Posts
    security:
      - BearerAuth: []
    parameters:
      - name: body
        in: body
        required: true
        schema:
          $ref: '#/definitions/Post'
    responses:
      201:
        description: Post actualizado exitosamente
        schema:
          $ref: '#/definitions/Post'
      400:
        description: Error al editar el post
    """

  id_usuario = get_jwt_identity()
  post = db.session.get(Post, id_post)

  if not post:
    return jsonify({"mensaje": "Post no encontrado"}), HTTPStatus.NOT_FOUND
  
  if post.id_usuario != id_usuario:
    return jsonify({"mensaje": "No tienes permisos para editar este post"}), HTTPStatus.FORBIDDEN

  try:
    json_data = request.get_json()
    if not json_data:
       return jsonify({"mensaje":"No hay datos proveidos"}), HTTPStatus.BAD_REQUEST
    datos = post_schema.load(json_data, session=db.session, partial=True)

    post.id_pais   = datos.pais      or post.id_pais
    post.titulo    = datos.titulo    or post.titulo
    post.contenido = datos.contenido or post.contenido

    db.session.commit()

    return jsonify(post_schema.dump(post)), HTTPStatus.OK

  except ValidationError as e:
    return jsonify({"error": e.messages}), HTTPStatus.BAD_REQUEST
  except Exception as err:
    return jsonify({"error": str(err)}), HTTPStatus.BAD_REQUEST              




# ------------------------ Endpoint para eliminar un Post ---------------------------- #
@post_bp.route('/del/<string:id_post>', methods=['DELETE'])
#@jwt_required()
def eliminar_post(id_post):
    """
    Eliminar un post

    Permite a un usuario autenticado eliminar su propio post.
    ---
    tags:
      - Posts
    security:
      - BearerAuth: []
    parameters:
      - name: id_post
        in: path
        type: string
        required: true
        description: ID del post a eliminar
    responses:
      200:
        description: Post eliminado exitosamente
      403:
        description: No tienes permisos para eliminar este post
      404:
        description: Post no encontrado
    """
    id_usuario = get_jwt_identity()
    post = Post.query.get(id_post)

    if not post:
        return jsonify({"mensaje": "Post no encontrado"}), HTTPStatus.NOT_FOUND

    if post.id_usuario != id_usuario:
        return jsonify({"mensaje": "No tienes permisos para eliminar este post"}), HTTPStatus.FORBIDDEN

    db.session.delete(post)
    db.session.commit()
    return jsonify({"mensaje": "Post eliminado exitosamente"}), HTTPStatus.OK



