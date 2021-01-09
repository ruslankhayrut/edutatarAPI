from marshmallow import Schema, fields, validate
from .constants import MIN_GRADE, MAX_GRADE


class StudentsGet(Schema):
    grade_num = fields.Int(validate=range(MIN_GRADE, MAX_GRADE), required=True)
    grade_litera = fields.String(required=True)
