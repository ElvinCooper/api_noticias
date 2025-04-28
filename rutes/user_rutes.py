from flask import Blueprint, request, jsonify
from modelos.user_model import Usuario

from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from extensions import db
from datetime import timedelta
from werkzeug.security import check_password_hash, generate_password_hash
