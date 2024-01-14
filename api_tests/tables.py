# '''
# для хранения таблиц
# '''
#
# from sqlalchemy import  Boolean, Column, Integer, String
#
# from db import Model
#
# class Films(Model):
#
#     __tablename__ = "films" #указываем реальное название бд
#
#     '''
#     дальше описываем поля, но только те которыми мы будем пользоваться
#     '''
#
#     film_id = Column(Integer, primary_key=True) #через primary_key мы связываемся с другими таблицами, в описанных должен быть primary_key
#     status = Column(String,index = True) # index = True , потому что это поле индексированное,нужно для выбора типа сортировки под капотом
#     title = Column(String)
#     is_premiere = Column(Boolean)
#
# class ItemType(Model):
#     __tablename__ = "item_type"
#     item_id = Column(Integer,primary_key=True)
#     item_type = Column(String)