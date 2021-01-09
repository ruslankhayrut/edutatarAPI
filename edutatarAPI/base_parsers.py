

class TableParser:
    """
    Parses raw html into struct -> {'header': List[], 'data': List[List[]]}
    """
    def __init__(self, html):
        self.html = html
        self.__data = {
            'header': [],
            'body': []
        }

    def parse(self):

        header_row = self.html.find('thead').find_all('tr')[-1].find_all('td')
        body_rows = self.html.find('tbody').find_all('tr')

        self.__data['header'] = [cell.text.strip().replace('\n', ' ') for cell in header_row]
        body = []
        for row in body_rows:
            cells = row.find_all('td')
            values = [cell.text.strip().replace('\n', ' ') for cell in cells]
            body.append(values)

        self.__data['body'] = body
        return self.__data
