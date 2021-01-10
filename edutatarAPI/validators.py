from marshmallow import Schema, fields, validates_schema, ValidationError, validate


class StudentsGet(Schema):
    grade = fields.String(missing=None)
    student = fields.String(missing=None)

    @validates_schema
    def validate_not_empty(self, data, **kwargs):
        if not data.items():
            raise ValidationError('AT least one parameter should be passed')


class MarksGet(Schema):
    grade = fields.String(required=True)
    term = fields.Int(validate=validate.Range(1, 4), required=True)
    subject = fields.String(required=True)
    student = fields.String(missing=None)
