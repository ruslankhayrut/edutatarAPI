import requests
from .students import Students
from .constants import UNAUTHORIZED_MSG
from .grades import Grades
from .subjects import Subjects
from .marks import Marks


class EduTatarAPI:
    def __init__(self, login, password):
        self.login = login
        self.password = password

        self.resource_handlers = {
            'students': Students,
            'marks': Marks,
            'homeworks': None,
            'grades': Grades,
            'subjects': Subjects
        }

    def __authenticate(self):
        s = requests.Session()

        s.headers.update({"Host": "edu.tatar.ru",
                          "Origin": "https://edu.tatar.ru",
                          "User-Agent": "User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_0) \
                                                AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 \
                                                YaBrowser/18.10.1.382 (beta) Yowser/2.5 Safari/537.36"
                          })
        h = {"Referer": "https://edu.tatar.ru/start/logon-process", "Content-Type": "application/x-www-form-urlencoded"}

        r = s.post("https://edu.tatar.ru/logon", headers=h,
                   data={
                       "main_login": self.login,
                       "main_password": self.password}
                   )

        if 'Личный кабинет' not in r.text:
            raise PermissionError
        return s

    def get(self, resource: str, **kwargs):
        params = kwargs.get('params', {})

        handler = self.resource_handlers.get(resource)
        if not handler:
            return {'status': 404, 'message': 'Resource not found'}

        try:
            session = self.__authenticate()
            res = handler(session).get(params)
        except NotImplementedError:
            return {'status': 405, 'message': 'Method not allowed'}
        except PermissionError:
            return {'status': 401, 'message': UNAUTHORIZED_MSG}

        return res

    def post(self, resource: str, json: dict):
        handler = self.resource_handlers.get(resource)
        if not handler:
            return {'status': 404, 'message': 'Resource not found'}

        try:
            session = self.__authenticate()
            res = handler(session).post(json)
        except NotImplementedError:
            return {'status': 405, 'message': 'Method not allowed'}
        except PermissionError:
            return {'status': 401, 'message': UNAUTHORIZED_MSG}

        return res
