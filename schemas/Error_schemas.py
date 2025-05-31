from marshmallow import Schema, fields



# --------------------- Schema para documentar errores --------------------------#
class ErrorSchema(Schema):
    success = fields.Boolean(load_default=False)
    message = fields.String(required=True)   