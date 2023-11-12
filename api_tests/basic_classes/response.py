from jsonschema import validate
from api_tests.global_enums import global_error_messages

class Response:

    def __init__(self,response):
        self.response = response
        self.response_json = response.json()
        self.response_status_code = response.status_code
        # self.expected = None

    def assert_status_code(self,status_code):
        # self.expected = status_code
        if isinstance(status_code,list):
            assert self.response_status_code in status_code, global_error_messages.wrong_value(self.response_status_code,status_code)
        else:
            assert self.response_status_code == status_code, global_error_messages.wrong_value(self.response_status_code,status_code)
            # assert self.response_status_code == status_code, self
        return self
    
    def validate(self,schema):
        # self.expected = schema
        validate(self.response_json,schema)

    # можно сделать так, тогда не нужно в глобал енамс делать лямбду. Нужно в ассерте возвращать self
    # def __str__(self):
    #     return (f'\nExpected = {self.expected}\n\n'
    #             f'status code = {self.response_status_code}\n'
    #             f'Request url = {self.response.url}\n'
    #             f'Responce body = {self.response_status_code}')
