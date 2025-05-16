from flask import jsonify
from flask_jwt_extended import JWTManager
from modelos.TokenBlocklist_model import TokenBlocklist
from extensions import db, jwt



@jwt.token_in_blocklist_loader
def check_if_token_revoked(jwt_header, jwt_payload):
    jti = jwt_payload["jti"]
    return db.session.query(TokenBlocklist.id).filter_by(jti=jti).scalar() is not None

@jwt.revoked_token_loader
def revoked_token_callback(jwt_header, jwt_payload):
    return jsonify({"mensaje": "El token ha sido revocado"}), 401
