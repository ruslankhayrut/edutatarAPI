from edutatarAPI import EduTatarAPI
from pprint import pprint

api = EduTatarAPI(login='5162000568', password='Huawei+#1')
pprint(api.get('grades'))
