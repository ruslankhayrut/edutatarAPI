from .abc import AbstractModel, AbstractParser
from .validators import StudentsGet
from marshmallow import ValidationError
from .constants import STUDENTS_PAGE_URL, NUMBERS_RE, NAMES_RE
from .grades import Grades
import re


class Students(AbstractModel):
    def get(self, params):
        try:
            params = StudentsGet().load(params)
        except ValidationError as err:
            return {'message': err.messages, 'status': 400}

        grade = params['grade']
        res = _StudentsParser(self.session, grade).json
        return res


class _StudentsParser(AbstractParser):
    def __init__(self, session, grade):
        super(_StudentsParser, self).__init__(session, page_url=STUDENTS_PAGE_URL)
        self.grade = grade.upper()

    def __get_students_list(self):
        grades_list = Grades(self.session).get(params={})
        grade = list(filter(lambda grade: str(grade['number']) + grade['litera'] == self.grade, grades_list))
        if not grade:
            return []

        grade_id = grade[0]['id']
        html = self.get_page_html(id=grade_id)

        matches = re.findall(r'addUser(.*)', str(html))

        students = []
        for match in matches:
            name = re.search(NAMES_RE, match)
            id = re.findall(NUMBERS_RE, match)
            if name and id:
                students.append({
                    'grade': self.grade,
                    'name': name.group(),
                    'id': int(id[1])
                })

        return students

    @property
    def json(self):
        students_list = self.__get_students_list()
        if not students_list:
            return {'message': 'Not found', 'status': 404}

        return students_list
