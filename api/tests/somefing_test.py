import pytest
import requests
from api.configuration import get_lib_forms,pub_libs
from api.basic_classes.response import Response
from api.schemas.pub_lib_v1 import Model_V1
from api.schemas.pub_lib_v2 import Model_v2

from api.global_enums import Statuses
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

@pytest.mark.parametrize("status, balance, avatar",[
    ("DONE",1,"Anu"),
    ("CLOSED",0,"Opa"),
    ("PANDING",-1,"Popa")
])
def test_with_generator_example(status, balance, avatar,get_player_generator):
    print(get_player_generator.set_avatar(avatar).set_status(status).sel_balance(balance).build())
    '''
    PASSED         [ 77%]{'balance': 1, 'avatar': 'Anu', 'account_status': 'DONE', 'localize': {'en': {'nickname': 'John'}, 'ru': {'nickname': 'Остап'}}}
    PASSED       [ 88%]{'balance': 0, 'avatar': 'Opa', 'account_status': 'CLOSED', 'localize': {'en': {'nickname': 'Kevin'}, 'ru': {'nickname': 'Серафим'}}}
    PASSED    [100%]{'balance': -1, 'avatar': 'Popa', 'account_status': 'PANDING', 'localize': {'en': {'nickname': 'Michael'}, 'ru': {'nickname': 'Татьяна'}}}
    '''
@pytest.mark.parametrize("delete_key",[
    ("balance"),
    ("avatar"),
    ("account_status"),
    ("localize")
])
def test_with_generator_example_delete_field(delete_key,get_player_generator):
    object_to_send = get_player_generator.build()
    del object_to_send[delete_key]
    print(object_to_send)
    '''
    PASSED [ 76%]{'avatar': 'https://google.com/', 'account_status': 'ACTIVE', 'localize': {'en': {'nickname': 'Brandon'}, 'ru': {'nickname': 'Регина'}}}
    PASSED [ 84%]{'balance': 0, 'account_status': 'ACTIVE', 'localize': {'en': {'nickname': 'Katrina'}, 'ru': {'nickname': 'Симон'}}}
    PASSED [ 92%]{'balance': 0, 'avatar': 'https://google.com/', 'localize': {'en': {'nickname': 'Jennifer'}, 'ru': {'nickname': 'Наина'}}}
    PASSED [100%]{'balance': 0, 'avatar': 'https://google.com/', 'account_status': 'ACTIVE'}
    '''

from api.generators.player_localizations import PLayerLocalization
def test_with_change_generator(get_player_generator):
    object_to_send = get_player_generator.update_inner_generator(
        'localize',PLayerLocalization('fr_FR')
    ).build()
    print(object_to_send)

    '''
    PASSED                      [100%]{'balance': 0, 'avatar': 'https://google.com/', 'account_status': 'ACTIVE', 'localize': {'en': {'nickname': 'Élise'}}}
    '''
@pytest.mark.parametrize("localizations,loc",[
    ("fr","fr_FR"),
    ("ru","ru_RU"),
    ("ar","ar_SA")
])
def test_with_example_new_bilder(get_player_generator,localizations,loc):
    # object_to_send = get_player_generator.update_inner_value(
    #     ['localize',"opa","popa","end"], "some value"
    # ).build()
    # print(object_to_send) #somefing_test.py::test_with_example_new_bilder PASSED                    [100%]{'balance': 0, 'avatar': 'https://google.com/', 'account_status': 'ACTIVE', 'localize': {'en': {'nickname': 'Claudia'}, 'ru': {'nickname': 'Капитон'}, 'opa': {'popa': {'end': 'some value'}}}}

    # object_to_send_with_object = get_player_generator.update_inner_value(
    #     ['localize', "opa", "popa", "end"], PLayerLocalization('fr_FR').build()
    # ).build()
    # print(object_to_send_with_object) #{'balance': 0, 'avatar': 'https://google.com/', 'account_status': 'ACTIVE', 'localize': {'en': {'nickname': 'Alicia'}, 'ru': {'nickname': 'Дарья'}, 'opa': {'popa': {'end': {'nickname': 'Dorothée'}}}}}
    object_to_send_localizations = get_player_generator.update_inner_value(
        ['localize', localizations], PLayerLocalization(loc).build()
    ).build()
    print(object_to_send_localizations)
    '''
    PASSED          [ 33%]{'balance': 0, 'avatar': 'https://google.com/', 'account_status': 'ACTIVE', 'localize': {'en': {'nickname': 'Patrick'}, 'ru': {'nickname': 'Кондратий'}, 'fr': {'nickname': 'Célina'}}}
    PASSED          [ 66%]{'balance': 0, 'avatar': 'https://google.com/', 'account_status': 'ACTIVE', 'localize': {'en': {'nickname': 'Nicholas'}, 'ru': {'nickname': 'Евстигней'}}}
    PASSED          [100%]{'balance': 0, 'avatar': 'https://google.com/', 'account_status': 'ACTIVE', 'localize': {'en': {'nickname': 'Gwendolyn'}, 'ru': {'nickname': 'Зоя'}, 'ar': {'nickname': 'مسلم'}}}
    '''

from api.schemas.computer import Computer
from api.examples import computer

def test_pydantic_object():
    comp = Computer.parse_obj(computer) #теперь через точку можно добраться к любому параметру в объекте
    print(comp.detailed_info)
    print(comp.detailed_info.physical.photo)
    '''
    здесь можно ассертами добить изщренные кейсы, чтоб не тулить все это в схему
    '''
    print(comp.detailed_info.physical.color.as_hex) #можно получить хекс цвета

@pytest.mark.parametrize("status",Statuses)
def test_with_auto_Statuses_parsing(status,get_player_generator):
    object_to_send = get_player_generator.set_status(status).build()
    print(object_to_send)




# '''
# ПРИМЕРЫ ТЕСТОВ С ТАБЛИЦА - РАБОТАТЬ НЕ БУДУТ, Т.К. НАДО ВАЛИДНУЮ ССЫЛКУ К БАЗЕ ВСТАВИТЬ В CONNECTION_ROW
# '''
# import tables as tables
#
#
#
# def test_get_data_films(get_db_session):
#     '''
#     пример селекта чего то из базы
#     '''
#     data = get_db_session.query(tables.Films).first()
#     print(data.title) #так можно получать данные из базы
#
# def test_try_to_delete_something(get_delete_method,get_db_session):
#     '''
#     пример использования метода для удаления чего из базы
#     '''
#     get_delete_method(get_db_session,tables.ItemType,(tables.ItemType.item_id==3))
#
# def test_try_to_add_testdata(get_db_session,get_add_method):
#     '''
#     пример использования метода для добавления чего из базы
#     '''
#     new_item_type = {"item_tye" : "NY_NEW_TYPE"} #что добавляем, по описанной нами модели - в частности названия полей должны совпадать
#     item = tables.ItemType(**new_item_type) #распаковываем
#     get_add_method(get_db_session,item)
#     print(item.item_id) #здесь поулчим id элемента который добавили
#
# def test_auto_add_testdata(get_db_session,get_add_method,get_item_type_generator):
#     '''
#     пример использования метода для добавления чего из базы + билдера объектов
#     '''
#     item = tables.ItemType(**get_item_type_generator.build()) #распаковываем
#     get_add_method(get_db_session,item)
#     print(item.item_id) #здесь поулчим id элемента который добавили
#
# def test_try_to_add_testdata(generate_item_type):
#     '''
#     пример использования комбинированной фикстуры, здесь мы создаем запись в дате - выполняем тест
#     в нашем случае просто принтим айди и сразу удаляем запись
#     '''
#     print(generate_item_type.item_id) da