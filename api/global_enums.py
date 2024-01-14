from enum import Enum
from basic_classes.pyenum import PyEnum
class global_error_messages(Enum):
    status_code_error = lambda actual, expected, env: f'BAD STATUS_CODE version = {env} actual = {actual} expected = {expected}'
class Statuses(PyEnum):
    ACTIVE = "ACTIVE"
    BANNED = "BANNED"
    DELETED = "DELETED"
    INACTTIVE = "INACTTIVE"


'''
сдеали глобал класс PyEnum для того, чтобы преобразовывать поля объекта в лист для передачи в parametrize
'''
# print(Statuses.list()) #['ACTIVE', 'BANNED', 'DELETED', 'INACTTIVE']