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
    def __init__(self, session):
        self.session = session

    def get_page_html(self, page_url, **kwargs):
        r = self.session.get(page_url, params=kwargs)
        html = BeautifulSoup(r.text, 'html.parser')
        return html

    @property
    def json(self):
        raise NotImplementedError
