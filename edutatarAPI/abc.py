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

    @staticmethod
    def find_subject_ids_from_selector(html, subject_name):
        subjects_selector = html.find('select', {'id': 'criteria'})
        if not subjects_selector:
            return []

        options = subjects_selector.find_all('option')
        subject_ids = []
        for option in options:
            if subject_name in option.text.replace(u'\xa0', ' '):
                subject_ids.append(option.get('value'))
        return subject_ids

    @property
    def json(self):
        raise NotImplementedError
