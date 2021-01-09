from .abc import AbstractModel, AbstractParser
from .validators import StudentsGet
from marshmallow import ValidationError


class Students(AbstractModel):
    def get(self, params):
        try:
            params = StudentsGet().load(params)
        except ValidationError as err:
            return {'message': err.messages, 'status': 400}

        grade = params['grade_num'] + params['grade_litera']
        res = _StudentsParser(self.session, grade).json
        return res


class _StudentsParser(AbstractParser):
    def __init__(self, session, grade):
        super(_StudentsParser, self).__init__(session)
        self.grade = grade

    @property
    def json(self):
        return {'message': 'hi'}
