import pytest
import requests
from configuration import get_lib_forms,pub_libs
from basic_classes.response import Response
from schemas.pub_lib_v1 import Model_V1
from schemas.pub_lib_v2 import Model_v2

def test_get_lib_export_data(parse_version):
    '''
    для parse_version проверка статус кода + для 1 и 2 валидация полей jsonа из ответа
    '''
    for version in parse_version:
        for lib in pub_libs:
            req = requests.get(f'{get_lib_forms+lib}?v={version}')
            if version == 3:
                Response(req).assert_status_code(200)
            else: Response(req).assert_status_code(200).validate(Model_V1 if version == 1 else Model_v2)
    print("test")
@pytest.mark.dev
@pytest.mark.parametrize("first_param, second_param, result",[
    (1,2,4),
    (-1,1,0),
    (-1,-2,-3),
    ("a","b","ab"),
    ("a",1,TypeError)
])
def test_parametrize_example(first_param,second_param,result):
    try:
        assert first_param+second_param == result
    except TypeError:
        if first_param == "a" and second_param == 1:
            pass
        else:
            print("bad")
