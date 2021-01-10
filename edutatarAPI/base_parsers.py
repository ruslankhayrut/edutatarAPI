import re
from .constants import NUMBERS_RE


class TableCell:
    def __init__(self, text: str, links: list = None):
        self.__text = text
        self.links = links if links is not None else []

    @property
    def value(self):
        if self.__text.isdigit():
            return int(self.__text)
        return self.__text

    def extract_id_from_link(self):
        if not self.links:
            return -1

        matches = re.findall(NUMBERS_RE, self.links[0])
        if matches:
            return matches[-1]
        return -1


class ParsedTable:
    def __init__(self, header: list, body: list):
        self.header = header
        self.body = body

    def jsonify(self, keys_mapping):
        items = []
        for row in self.body:
            d = {}
            for header_key, cell in zip(self.header, row):
                dict_key = keys_mapping.get(header_key)
                if dict_key:
                    d.update({dict_key: cell.value})
            items.append(d)
        return items


class TableParser:
    """
    Parses raw html into ParsedTable instance
    """
    def __init__(self, html):
        self.html = html

    @staticmethod
    def _extract_cell_data(cell) -> TableCell:
        text = cell.text.strip().replace('\n', ' ')
        hrefs = cell.find_all('a', href=True)
        links = []
        if hrefs:
            links = [link.get('href') for link in hrefs]
        table_cell = TableCell(text, links)
        return table_cell

    def parse(self) -> ParsedTable:
        header_row = self.html.find('thead').find_all('tr')[-1].find_all('td')
        body_rows = self.html.find('tbody').find_all('tr')

        header = [cell.text.strip().replace('\n', ' ') for cell in header_row]
        body = []
        for row in body_rows:
            cells = row.find_all('td')
            values = [self._extract_cell_data(cell) for cell in cells]
            body.append(values)

        parsed_table = ParsedTable(header, body)
        return parsed_table

