from flask import Blueprint, request, jsonify
from modelos.post_model import Post
from modelos.post_categoria_model import PostCategoria
from modelos.categoria_model import Categoria
from schemas.simple.post_simple_schema import PostSimpleSchema
from schemas.post_schema import PostSchema
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from extensions import db
from werkzeug.security import check_password_hash, generate_password_hash
from http import HTTPStatus
from modelos.pais_model import Pais
from marshmallow.exceptions import ValidationError




post_bp = Blueprint('post', __name__)

# Esquemas para Serializacion/Deserializacion
post_schema = PostSchema()
posts_schemas = PostSchema(many=True)


#---------------------- Enpoint para consultar todos los post en la BD --------------------------#
@post_bp.route('/posts', methods=['GET'])
@jwt_required() 
def get_all_post():
  """
    Obtener todos los posts
    ---
    tags:
      - Posts
    responses:
      200:
        description: Lista de posts
        schema:
          type: array
          items:
            $ref: '#/definitions/Post'
  """
  #posts = Post.query.all()
  posts = Post.query.paginate(page=1, per_page=10, error_out=False)
  return jsonify({
                "posts": posts_schemas.dump(posts.items, many=True),
                "pagina_actual": posts.page,
                "total_paginas": posts.pages}), HTTPStatus.OK





#------------------------ Enpoint consultar un post con su id ----------------------#
@post_bp.route('post//<string:id_post>', methods=['GET'])
def get_post_by_user(id_post):
    """
    Obtener un post por ID

    Retorna los detalles de un post específico según su ID.
    ---
    tags:
      - Posts
    parameters:
      - name: id_post
        in: path
        type: string
        required: true
        description: ID del post
    responses:
      200:
        description: Post encontrado
        schema:
          $ref: '#/definitions/Post'
      404:
        description: Post no encontrado
    """
    
    post = db.session.get(Post, id_post)

    if not post:
      return jsonify({"mensaje": "Post no encontrado"}), HTTPStatus.NOT_FOUND  

    return jsonify(post_schema.dump(post)), HTTPStatus.OK



# ---------------------------  Endpoint para crear un nuevo Post -----------------------------#
@post_bp.route('/create', methods=['POST'])
@jwt_required()
def crear_post():
    
  """
  Crear un nuevo post

  Permite a un usuario autenticado crear un nuevo post.
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
      description: Post creado exitosamente
      schema:
        $ref: '#/definitions/Post'
    400:
      description: Error al crear el post
  """
    
  json_data = request.get_json()
  user_id = get_jwt_identity()
  
  try:
    json_data['id_usuario'] = user_id
    id_pais = json_data['id_pais']
    categoria_ids = json_data.pop('categorias', [])

    # validar la existencia del pais
    pais = Pais.query.filter_by(id_pais=id_pais).first()  #validar si el codigo de pais recibido existe
    if not pais:
       return jsonify({"error": "El id_pais digitado no existe en el catalogo, favor revisar"})
    
    # validar existencia de cada categoria
    categorias_validas = []
    for id_categoria in categoria_ids:
      if Categoria.query.get(id_categoria):
        categorias_validas.append(id_categoria)
      else:
         continue
    
    
    # crear el post
    nuevo_post = post_schema.load(json_data)
    db.session.add(nuevo_post)
    db.session.flush()  # para tener el ID del post antes del commit

    # Insertar relaciones
    for id_categoria in categorias_validas:
       relacion = PostCategoria(id_post=nuevo_post.id_post, id_categoria=id_categoria)
       db.session.add(relacion)

    db.session.commit()
    return jsonify(post_schema.dump(nuevo_post)), HTTPStatus.CREATED
  
  except Exception as e:
      db.session.rollback()
      return jsonify({'error': str(e)}), HTTPStatus.BAD_REQUEST
  


#------------------------ Actualizar o Editar  un Post -----------------------------#
@post_bp.route('/update/<string:id_post>', methods=['PUT'])
@jwt_required()
def actualizar_post(id_post):

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
@jwt_required()
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



