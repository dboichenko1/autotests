import pytest
import requests
from configuration import get_lib_forms,pub_libs
from basic_classes.response import Response
from schemas.pub_lib_v1 import Model_V1
from schemas.pub_lib_v2 import Model_v2


# def test_get_lib_export_data(parse_version):
#     '''
#     для parse_version проверка статус кода + для 1 и 2 валидация полей jsonа из ответа
#     '''
#     for version in parse_version:
#         for lib in pub_libs:
#             req = requests.get(f'{get_lib_forms+lib}?v={version}')
#             if version == 3:
#                 Response(req).assert_status_code(200)
#             else: Response(req).assert_status_code(200).validate(Model_V1 if version == 1 else Model_v2)
#     print("test")
# @pytest.mark.dev
# @pytest.mark.parametrize("first_param, second_param, result",[
#     (1,2,4),
#     (-1,1,0),
#     (-1,-2,-3),
#     ("a","b","ab"),
#     ("a",1,TypeError)
# ])
# def test_parametrize_example(first_param,second_param,result):
#     try:
#         assert first_param+second_param == result
#     except TypeError:
#         if first_param == "a" and second_param == 1:
#             pass
#         else:
#             print("bad")
#
# @pytest.mark.parametrize("status, balance, avatar",[
#     ("DONE",1,"Anu"),
#     ("CLOSED",0,"Opa"),
#     ("PANDING",-1,"Popa")
# ])
# def test_with_generator_example(status, balance, avatar,get_player_generator):
#     print(get_player_generator.set_avatar(avatar).set_status(status).sel_balance(balance).build())
#     '''
#     PASSED         [ 77%]{'balance': 1, 'avatar': 'Anu', 'account_status': 'DONE', 'localize': {'en': {'nickname': 'John'}, 'ru': {'nickname': 'Остап'}}}
#     PASSED       [ 88%]{'balance': 0, 'avatar': 'Opa', 'account_status': 'CLOSED', 'localize': {'en': {'nickname': 'Kevin'}, 'ru': {'nickname': 'Серафим'}}}
#     PASSED    [100%]{'balance': -1, 'avatar': 'Popa', 'account_status': 'PANDING', 'localize': {'en': {'nickname': 'Michael'}, 'ru': {'nickname': 'Татьяна'}}}
#     '''
# @pytest.mark.parametrize("delete_key",[
#     ("balance"),
#     ("avatar"),
#     ("account_status"),
#     ("localize")
# ])
# def test_with_generator_example_delete_field(delete_key,get_player_generator):
#     object_to_send = get_player_generator.build()
#     del object_to_send[delete_key]
#     print(object_to_send)
#     '''
#     PASSED [ 76%]{'avatar': 'https://google.com/', 'account_status': 'ACTIVE', 'localize': {'en': {'nickname': 'Brandon'}, 'ru': {'nickname': 'Регина'}}}
#     PASSED [ 84%]{'balance': 0, 'account_status': 'ACTIVE', 'localize': {'en': {'nickname': 'Katrina'}, 'ru': {'nickname': 'Симон'}}}
#     PASSED [ 92%]{'balance': 0, 'avatar': 'https://google.com/', 'localize': {'en': {'nickname': 'Jennifer'}, 'ru': {'nickname': 'Наина'}}}
#     PASSED [100%]{'balance': 0, 'avatar': 'https://google.com/', 'account_status': 'ACTIVE'}
#     '''

from generators.player_localizations import PLayerLocalization
def test_with_change_generator(get_player_generator):
    object_to_send = get_player_generator.update_inner_generator(
        'localize',PLayerLocalization('fr_FR')
    ).build()
    print(object_to_send)

    '''
    PASSED                      [100%]{'balance': 0, 'avatar': 'https://google.com/', 'account_status': 'ACTIVE', 'localize': {'en': {'nickname': 'Élise'}}}
    '''