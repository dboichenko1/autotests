from enum import Enum
class global_error_messages(Enum):
    wrong_value = lambda actual, expected : f'Recieved status code is not equal to expected actual = {actual} expected = {expected}'