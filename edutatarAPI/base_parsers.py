class ParsedTable:
    def __init__(self, header: list, body: list):
        self.header = header
        self.body = body

    def jsonify(self, keys_mapping):
        items = []
        for row in self.body:
            d = {}
            for header_key, value in zip(self.header, row):
                dict_key = keys_mapping.get(header_key)
                if dict_key:
                    if value.isdigit():
                        value = int(value)
                    d.update({dict_key: value})
            items.append(d)
        return items


class TableParser:
    """
    Parses raw html into ParsedTable instance
    """
    def __init__(self, html):
        self.html = html

    def parse(self):

        header_row = self.html.find('thead').find_all('tr')[-1].find_all('td')
        body_rows = self.html.find('tbody').find_all('tr')

        header = [cell.text.strip().replace('\n', ' ') for cell in header_row]
        body = []
        for row in body_rows:
            cells = row.find_all('td')
            values = [cell.text.strip().replace('\n', ' ') for cell in cells]
            body.append(values)

        parsed_table = ParsedTable(header, body)
        return parsed_table

