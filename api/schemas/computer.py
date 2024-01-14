
'''
Пример валидирования следующего jsona:
'''
# computer = {
#     "id": 21,
#     "status": "ACTIVE",
#     "activated_at": "2013-06-01",
#     "expiration_at": "2040-06-01",
#     "host_v4": "91.192.222.17",
#     "host_v6": "2001:0db8:85a3:0000:0000:8a2e:0370:7334",
#     "detailed_info": {
#         "physical": {
#             "color": 'green',
#             "photo": 'https://images.unsplash.com/photo-1587831990711-23ca6441447b?ixlib=rb-1.2.1&ixid=MnwxMjA3fDB8MHxzZWFyY2h8MXx8ZGVza3RvcCUyMGNvbXB1dGVyfGVufDB8fDB8fA%3D%3D&w=1000&q=80',
#             "uuid": "73860f46-5606-4912-95d3-4abaa6e1fd2c"
#         },
#         "owners": [{
#             "name": "Stephan Nollan",
#             "card_number": "4000000000000002",
#             "email": "shtephan.nollan@gmail.com",
#         }]
#     }
# }


from pydantic import BaseModel
from pydantic.types import PastDate,FutureDate
from global_enums import Statuses
from pydantic.networks import IPv4Address,IPv6Address

from schemas.detailedInfo import DetailedInfo

from examples import computer

class Computer(BaseModel):
    id: int
    status: Statuses
    activated_at: PastDate # проверка что это дата меньше чем текущая
    expiration_at: FutureDate #проверка что эта дата больше чем текущая
    host_v4: IPv4Address #валидация ip
    host_v6: IPv6Address
    detailed_info: DetailedInfo

# #example:
# comp = Computer.parse_obj(computer)
# print(comp)
# '''
# id=21 status=<Statuses.ACTIVE: 'ACTIVE'> activated_at=datetime.date(2013, 6, 1) expiration_at=datetime.date(2040, 6, 1) host_v4=IPv4Address('91.192.222.17') host_v6=IPv6Address('2001:db8:85a3::8a2e:370:7334') detailed_info=DetailedInfo(physical=Physical(color=Color('green', rgb=(0, 128, 0)), photo=Url('https://images.unsplash.com/photo-1587831990711-23ca6441447b?ixlib=rb-1.2.1&ixid=MnwxMjA3fDB8MHxzZWFyY2h8MXx8ZGVza3RvcCUyMGNvbXB1dGVyfGVufDB8fDB8fA%3D%3D&w=1000&q=80'), uuid=UUID('73860f46-5606-4912-95d3-4abaa6e1fd2c')), owners=[Owners(name='Stephan Nollan', card_number='4000000000000002', email='shtephan.nollan@gmail.com')])
# '''
# '''
# также при необходимости можно из этого объекта сгенерить  json схему чтобы убедиться что она абсолютна не читаема и неподлежит изменениям)
# '''
# print(comp.schema_json())