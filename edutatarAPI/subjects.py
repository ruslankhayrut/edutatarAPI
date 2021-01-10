from .abc import AbstractModel, AbstractParser
from .constants import SUBJECTS_PAGE_URL
from .models import Subject

class Subjects(AbstractModel):
    def get(self, params):
        res = _SubjectsParser(self.session).json
        return res


class _SubjectsParser(AbstractParser):
    def __init__(self, session):
        super(_SubjectsParser, self).__init__(session, page_url=SUBJECTS_PAGE_URL)

    def __find_checked_items(self):
        html = self.get_page_html()
        form = html.find('form', {'action': self.page_url})
        checked_subjs = form.find_all('input', {'checked': 'checked'})
        return checked_subjs

    @property
    def json(self):
        checked_items = self.__find_checked_items()
        labels = [item.parent.text for item in checked_items]
        labels.sort()
        objects = [Subject(name=label) for label in labels]
        return objects
