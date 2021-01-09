from .abc import AbstractModel, AbstractParser
from .constants import GRADES_PAGE_URL
from .base_parsers import TableParser


class Grades(AbstractModel):
    def get(self, params):
        res = _GradesParser(self.session).json
        return res


class _GradesParser(AbstractParser):
    def __init__(self, session):
        super(_GradesParser, self).__init__(session, page_url=GRADES_PAGE_URL)
        self.header_to_key = {
            'Номер класса': 'grade_number',
            'Литера': 'litera',
            'Руководитель': 'class_teacher'
        }

    def __find_grades_table(self):
        html = self.get_page_html()
        table = html.find('table', {'class': 'table', 'id': 'dataTable'})
        return table

    @property
    def json(self):
        grades_table = self.__find_grades_table()
        parsed_table = TableParser(grades_table).parse()
        res = parsed_table.jsonify(self.header_to_key)
        return res
