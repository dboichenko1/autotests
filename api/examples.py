computer = {
    "id": 21,
    "status": "ACTIVE",
    "activated_at": "2013-06-01",
    "expiration_at": "2040-06-01",
    "host_v4": "91.192.222.17",
    "host_v6": "2001:0db8:85a3:0000:0000:8a2e:0370:7334",
    "detailed_info": {
        "physical": {
            "color": 'green',
            "photo": 'https://images.unsplash.com/photo-1587831990711-23ca6441447b?ixlib=rb-1.2.1&ixid=MnwxMjA3fDB8MHxzZWFyY2h8MXx8ZGVza3RvcCUyMGNvbXB1dGVyfGVufDB8fDB8fA%3D%3D&w=1000&q=80',
            "uuid": "73860f46-5606-4912-95d3-4abaa6e1fd2c"
        },
        "owners": [{
            "name": "Stephan Nollan",
            "card_number": "4000000000000002",
            "email": "shtephan.nollan@gmail.com",
        }]
    }
}

#
# from db import session
#
# import tables #удобный способ для взаимодействия со всеми таблицами
# #единственный нюанс, если в другом микросервисе проекта будет таблица с таким же названием, придется разбивать на разыне файлы
#
# result = session.query(tables.Films.film_id, tables.Films.title).first()
# result1 = session.query(tables.Films.film_id, tables.Films.title).all()
# result2 = session.query(tables.Films.film_id, tables.Films.title).one_or_none()
# '''
# .first() - возвращает первый результат
# .all() - возвращает все результаты (в виде массива таплов)
# .one_or_none() - должен соответствовать конретному условию и вернет либо его, либо ничего (возвращает в виде тапла)
# '''
# #пример как работают фильтры
# result3 = session.query(tables.Films.film_id, tables.Films.title).filter(tables.Films.film_id==180).one_or_none()
# #использование нескольких фильтров
# result4 = session.query(tables.Films.film_id, tables.Films.title).filter(
#     tables.Films.film_id > 100,
#     tables.Films.film_id < 150
# ).all()
#
# #запринтив такое можно посмотреть какой sql запрос сгенерен
# film_ids = session.query(tables.Films.film_id).filter(tables.Films.film_id > 180).subquery()
#
# #использоавли результат отдного фильтра в другом
# result5 = session.query(tables.Films.title).filter(tables.Films.film_id.in_(film_ids)).all()
#
# # сделать сортировку
# film_ids1 = session.query(
#     tables.Films.film_id,
#     tables.Films.title
# ).order_by(tables.Films.film_id).all()
#
# #для того чтоб сделать в обратном порядке
# from sqlalchemy.sql.expression import desc
# film_ids2 = session.query(
#     tables.Films.film_id,
#     tables.Films.title
# ).order_by(desc(tables.Films.film_id)).all()
#
# #лимитировать выборку
# film_ids3 = session.query(
#     tables.Films.film_id,
#     tables.Films.title
# ).order_by(desc(tables.Films.film_id)).limit(1).all()
#
# #пропускать определенного количество элементов
# film_ids4 = session.query(
#     tables.Films.film_id,
#     tables.Films.title
# ).order_by(desc(tables.Films.film_id)).limit(1).offset(1).all()