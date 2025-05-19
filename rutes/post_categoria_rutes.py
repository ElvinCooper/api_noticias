from flask import Blueprint, request, jsonify
from http import HTTPStatus
from schemas.post_categoria_schema import PostCategoriaSchema
from modelos.post_categoria_model import PostCategoria
from flask_jwt_extended import jwt_required



post_cat_bp = Blueprint('postCategoria', __name__)
post_cat_schema = PostCategoriaSchema()
post_cats_schemas = PostCategoriaSchema(many=True)



#--------------- Consultar todos los datos de la tabla ------------------------------#
@post_cat_bp.route('/postcat', methods=['GET'])
#@jwt_required()
def obtener_posts_categorias():
    """
    Obtener todas las parejas Post_Categoria

    Este endpoint retorna la lista completa de Post_Categorías existentes en el sistema.
    ---
    tags:
      - Post_Categoria
    responses:
      200:
        description: Lista de parejes Post-Categorías
        schema:
          type: array
          items:
            $ref: '#/definitions/Post_categorias'
    """
    post_cat = PostCategoria.query.all()
    return jsonify(post_cats_schemas(post_cat)), HTTPStatus.OK




# ----------------------------  Consultar un post_categoria por su ID  --------------------------------#
@post_cat_bp.route('/postcat/<string:id_post>', methods=['GET'])
#@jwt_required()
def obtener_post_cat_por_id(id_post):
    """
    Obtener una una pareja Post_Categoria por ID

    Este endpoint permite consultar los detalles de un Post_Categoría específica usando su ID.
    ---
    tags:
      - Post_Categoria
    parameters:
      - name: id_post
        in: path
        type: string
        required: true
        description: ID del Post_Categoría a consultar
    responses:
      200:
        description: Pareja encontrada encontrada
        schema:
          $ref: '#/definitions/Post_categorias'
      404:
        description: Post_Categoría no encontrada
    """
    post_cat = PostCategoria.query.filter_by(id_categoria=id_post).first()

    if not post_cat:
        return jsonify({"error": "Pareja Post_Categoria no encontrada"}), HTTPStatus.NOT_FOUND
    
    return jsonify(post_cat_schema.dump(post_cat)), HTTPStatus.OK
