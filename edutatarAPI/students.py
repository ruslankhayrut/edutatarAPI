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
        name = params['name']
        res = _StudentsParser(self.session, grade, name).json
        return res


class _StudentsParser(AbstractParser):
    def __init__(self, session, grade, name):
        super(_StudentsParser, self).__init__(session, page_url=STUDENTS_PAGE_URL)
        self.grade = grade
        self.name = name
        self.grades_list = Grades(self.session).get(params={})

    def __get_students_by_name(self):
        students = []
        for grade in self.grades_list:
            students += self.__get_students_by_grade(grade)
        return students

    def __get_students_by_grade(self, grade):
        grade_id = grade['id']
        grade_name = str(grade['number']) + grade['litera']

        html = self.get_page_html(id=grade_id)

        matches = re.findall(r'addUser(.*)', str(html))

        students = []
        for match in matches:
            if self.name:
                if self.name in match:
                    name = self.name
                else:
                    name = None
            else:
                name = re.search(NAMES_RE, match)
                name = name.group() if name else None

            id = re.findall(NUMBERS_RE, match)
            if name and id:
                students.append({
                    'grade': grade_name,
                    'name': name,
                    'id': int(id[1])
                })

        return students

    @property
    def json(self):
        if not self.grade and self.name:
            return self.__get_students_by_name()

        else:
            self.grade = self.grade.upper()
            grade = list(filter(lambda grade: str(grade['number']) + grade['litera'] == self.grade, self.grades_list))
            if not grade:
                return []

            grade = grade[0]
            return self.__get_students_by_grade(grade)


