from .abc import AbstractModel, AbstractParser
from .validators import StudentsGet
from marshmallow import ValidationError
from .constants import STUDENTS_PAGE_URL, NUMBERS_RE, NAMES_RE
from .grades import Grades
from .models import Student
import re


class Students(AbstractModel):
    def get(self, params):
        try:
            params = StudentsGet().load(params)
        except ValidationError as err:
            return {'message': err.messages, 'status': 400}

        grade = params['grade']
        student = params['student']
        res = _StudentsParser(self.session, grade, student).json
        return res


class _StudentsParser(AbstractParser):
    def __init__(self, session, grade, student):
        super(_StudentsParser, self).__init__(session, page_url=STUDENTS_PAGE_URL)
        self.grade = grade
        self.student = student

    def __get_students_by_name(self):
        students = []
        grades_list = Grades(self.session).get(params={})
        for grade in grades_list:
            students += self.__get_students_by_grade(grade)
        return students

    def __get_students_by_grade(self, grade):
        html = self.get_page_html(id=grade.id)

        matches = re.findall(r'addUser(.*)', str(html))

        students = []
        for match in matches:
            if self.student:
                if self.student in match:
                    name = self.student
                else:
                    name = None
            else:
                name = re.search(NAMES_RE, match)
                name = name.group() if name else None

            id = re.findall(NUMBERS_RE, match)
            if name and id:
                student_obj = Student(
                    id=int(id[1]),
                    grade=grade.name,
                    name=name
                )
                students.append(student_obj)

        return students

    @property
    def json(self):
        if not self.grade and self.student:
            return self.__get_students_by_name()

        else:
            required_grade = Grades(self.session).get(params={'grade': self.grade.upper()})
            if not required_grade:
                return []

            grade = required_grade[0]
            return self.__get_students_by_grade(grade)


