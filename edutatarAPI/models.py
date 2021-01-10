class Model:
    def as_dict(self):
        return vars(self)


class Subject(Model):
    def __init__(self, name):
        self.name = name


class Grade(Model):
    def __init__(self, id: int, number: int, litera: str, teacher: str):
        self.id = id
        self.number = number
        self.litera = litera
        self.teacher = teacher

    @property
    def name(self):
        return str(self.number) + self.litera


class Student(Model):
    def __init__(self, id, grade, name):
        self.id = id
        self.grade = grade
        self.name = name


class Mark(Model):
    def __init__(self, date, value):
        self.date = date
        self.value = value


