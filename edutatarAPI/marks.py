from .abc import AbstractModel, AbstractParser
from .validators import MarksGet
from marshmallow import ValidationError
from .constants import MARKS_PAGE_URL, NAMES_RE
from .grades import Grades
from .base_parsers import MarksTableParser
import re


class Marks(AbstractModel):
    def get(self, params):
        try:
            params = MarksGet().load(params)
        except ValidationError as err:
            return {'message': err.messages, 'status': 400}

        grade = params['grade']
        term = params['term']
        subject = params['subject']
        student = params['student']
        res = _MarksParser(self.session, grade, term, subject, student).json
        return res


class _MarksParser(AbstractParser):
    def __init__(self, session, grade, term, subject, student):
        super(_MarksParser, self).__init__(session, page_url=MARKS_PAGE_URL)
        self.grade = grade.upper()
        self.term = term
        self.subject = subject
        self.student = student
        self.required_grade = Grades(self.session).get(params={'grade': self.grade})[0]

    def get_pages_count(self, html):
        pages_selectors = html.find('p', {'class': 'pages'}).find_all('a')
        pages_count = len(pages_selectors)
        if pages_selectors[-1].text != '>>':
            return pages_count
        html = self.get_page_html(edu_class_id=self.required_grade.id, page=pages_count + 1)
        return pages_count + self.get_pages_count(html)

    def pages_generator(self, pages_count, subj_id):
        i = 1
        while i <= pages_count:
            html_page = self.get_page_html(edu_class_id=self.required_grade.id,
                                           term=self.term,
                                           page=i,
                                           criteria=subj_id)
            yield html_page
            i += 1

    @property
    def json(self):
        base_html = self.get_page_html(edu_class_id=self.required_grade.id, page=1)
        subject_ids = self.find_subject_ids_from_selector(base_html, self.subject)

        tables = []
        for subj_id in subject_ids:
            html = self.get_page_html(edu_class_id=self.required_grade.id,
                                      term=self.term,
                                      page=1,
                                      criteria=subj_id)
            teacher_block = html.find(text='Учитель:').find_parent('div').text
            teacher = re.search(NAMES_RE, teacher_block)
            if not teacher:
                return []
            teacher = teacher.group().strip()
            pages_count = self.get_pages_count(html)
            pages_to_parse = self.pages_generator(pages_count, subj_id)
            parsed_marks_table = MarksTableParser(pages_to_parse)

        return tables
