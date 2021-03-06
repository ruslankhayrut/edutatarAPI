from re import compile

MIN_GRADE = 1
MAX_GRADE = 11

UNAUTHORIZED_MSG = 'Не удалось войти в аккаунт. ' \
                   'Убедитесь, что вы верно ввели логин/пароль и двухфакторная аутентификация отключена.'

GRADES_PAGE_URL = '/school/academic_year/classes'
SUBJECTS_PAGE_URL = '/school/subject/index'
STUDENTS_PAGE_URL = '/school/academic_year/pupils'
MARKS_PAGE_URL = '/school/journal/school_editor'

NUMBERS_RE = compile(r'\d+')
NAMES_RE = compile(r'([А-ЯЁ][а-яё]+[\-\s]?){3,}')
