from enum import Enum
class global_error_messages(Enum):
    status_code_error = lambda actual, expected, env: f'BAD STATUS_CODE version = {env} actual = {actual} expected = {expected}'