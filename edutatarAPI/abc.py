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
        r = self.session.get(self.page_url, params=kwargs)
        html = BeautifulSoup(r.text, 'html.parser')
        return html

    @property
    def json(self):
        raise NotImplementedError
