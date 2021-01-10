from marshmallow import Schema, fields, validates_schema, ValidationError


class StudentsGet(Schema):
    grade = fields.String()
    name = fields.String()

    @validates_schema
    def validate_not_empty(self, data, **kwargs):
        if not data.items():
            raise ValidationError('AT least one parameter should be passed')
