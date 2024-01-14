# from sqlalchemy.orm import sessionmaker #для создания сессии
# from sqlalchemy import  create_engine #для создания движка
# from sqlalchemy.ext.declarative import declarative_base #для моделей
#
# from configuration import CONNECTION_ROW
# Model = declarative_base(name = "Model")
# '''
# Создаем экземпляр класса Model, который позволяет взаимодействовать
# с таблицы посредством Python
# возвращает класс, который переводит с python на sql
# для описания наших табличек
# '''
#
# #движок
# engine = create_engine(
#     CONNECTION_ROW
# )
#
# #для генерации сессий
# Session = sessionmaker(
#     engine,
#     autoflush=False, #автообновление данных в базе если нужно в реальном времени получить свежие запдейченые данные из базы надо поставить тру
#     autocomit = False
# )
#
# session = Session() #новую сессию получили