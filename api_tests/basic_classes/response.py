from jsonschema import validate
from global_enums import global_error_messages

class Response:

    def __init__(self,response):
        self.response = response
        self.response_json = response.json()
        self.response_status_code = response.status_code

    def assert_status_code(self,status_code):
        if isinstance(status_code,list):
            assert self.response_status_code in status_code, global_error_messages.wrong_value(self.response_status_code,status_code)
        else:
            assert self.response_status_code == status_code, global_error_messages.wrong_value(self.response_status_code,status_code)
        return self
    
    def validate(self,schema):
        validate(self.response_json,schema)