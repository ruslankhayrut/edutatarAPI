from marshmallow import Schema, fields, validate


class StudentsGet(Schema):
    grade = fields.String(required=True)
