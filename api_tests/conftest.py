from api_tests.generators.players import Player
import pytest


@pytest.fixture
def parse_version():
    return [1, 2, 3]


@pytest.fixture
def get_player_generator():
    return Player()

# from db import Session
# @pytest.fixture
# def get_db_session():
#     '''
#     для получения сессии к базе данных
#
#     '''
#     session = Session() #создали сессию
#     try:
#         yield session #отдали сессию в тест
#     finally:
#         session.close() #в любом случае сессию закрываем
#
#
# def delete_test_data(session,table,filter_data):
#     '''
#     универсальный метод для удаления данных из таблиц
#     '''
#     session.query(table).filter(filter_data).delete() #сделали обычный селект и в конце вызвали делет - удалили
#     session.commit() #закоммитили наши изменения
#
# @pytest.fixture
# def get_delete_method():
#     return delete_test_data #возвращает его как объект
#
# def add_method(session,item):
#     '''
#     универсальный метод для добавления чего то в бд
#     '''
#     session.add(item)
#     session.commit()
#
# @pytest.fixture
# def get_add_method():
#     return add_method #возвращает его как объект
#
# from api_tests.generators.item_type_generator import ItemsTypeBuilder
#
# @pytest.fixture
# def get_item_type_generator():
#     '''
#     для генерации объектов которые будут доабвляться в базу
#     '''
#     return ItemsTypeBuilder
#
# import tables
# @pytest.fixture
# def generate_item_type(get_db_session,get_item_type_generator,get_add_method,get_delete_method):
#     '''
#     Пример фикстуры которая использует другие фикстуры. С помощью этого примера
#     мы можем подготовить себе тестовые данные в базе, передать их в тест, а
#     уже после выполнения удалить.
#     '''
#     # item = tables.I
#     item = tables.ItemType(**get_item_type_generator.build())
#     get_add_method(get_db_session,item)
#     yield item
#     get_delete_method(get_db_session,tables.ItemType,(tables.ItemType.item_id == item.item_id))
