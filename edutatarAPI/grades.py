from .abc import AbstractModel, AbstractParser
from .constants import GRADES_PAGE_URL
from .base_parsers import TableParser


class Grades(AbstractModel):
    def get(self, params):
        res = _GradesParser(self.session).json
        return res


class _GradesParser(AbstractParser):
    def __init__(self, session):
        super(_GradesParser, self).__init__(session)
        self.page_url = GRADES_PAGE_URL
        self.header_to_key = {
            'Номер класса': 'grade_number',
            'Литера': 'litera',
            'Руководитель': 'class_teacher'
        }

    def __find_grades_table(self):
        html = self.get_page_html(self.page_url)
        table = html.find('table', {'class': 'table', 'id': 'dataTable'})
        return table

    @property
    def json(self):
        grades_table = self.__find_grades_table()
        structured_table = TableParser(grades_table).parse()
        header = structured_table['header']
        body = structured_table['body']

        items = []
        for item in body:
            d = {}
            for header_key, value in zip(header, item):
                dict_key = self.header_to_key.get(header_key)
                if dict_key:
                    if value.isdigit():
                        value = int(value)
                    d.update({dict_key: value})
            items.append(d)
        return items
