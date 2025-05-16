from extensions import db
import uuid
from datetime import datetime, timezone


class TokenBlocklist(db.Model):
    __tablename__ = "token_blocklist"

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    jti = db.Column(db.String(36), nullable=False, index=True, unique=True)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))