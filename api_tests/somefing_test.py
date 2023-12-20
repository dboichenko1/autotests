import requests
from configuration import get_lib_forms,pub_libs
from basic_classes.response import Response
from schemas.pub_lib_v1 import Model_V1
from schemas.pub_lib_v2 import Model_v2
parse_version = [1,2,3]
def test_get_lib_export_data():
    '''
    для parse_version проверка статус кода + для 1 и 2 валидация полей jsonа из ответа
    '''
    for version in parse_version:
        for lib in pub_libs:
            req = requests.get(f'{get_lib_forms+lib}?v={version}')
            if version == 3:
                Response(req).assert_status_code(200)
            else: Response(req).assert_status_code(200).validate(Model_V1 if version == 1 else Model_v2)