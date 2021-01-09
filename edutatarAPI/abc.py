from abc import ABC
from bs4 import BeautifulSoup


class AbstractModel(ABC):
    def __init__(self, session):
        self.session = session

    def get(self, params):
        raise NotImplementedError

    def post(self, json):
        raise NotImplementedError


class AbstractParser(ABC):
    def __init__(self, session, page_url=''):
        self.session = session
        self.page_url = page_url

    def get_page_html(self, **kwargs):
        url = 'https://edu.tatar.ru' + self.page_url

        r = self.session.get(url, params=kwargs)
        html = BeautifulSoup(r.text, 'html.parser')
        return html

    def build_query_string(self, **kwargs):
        base_url = self.page_url
        pairs = []
        for key, val in kwargs.items():
            pair = f'{key}={val}'
            pairs.append(pair)

        if not pairs:
            return base_url

        query_string = '&'.join(pairs)
        return base_url + '?' + query_string

    @property
    def json(self):
        raise NotImplementedError
