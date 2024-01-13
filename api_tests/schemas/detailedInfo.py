'''
аналогично вынесли из compute.py
'''
from pydantic import BaseModel
from pydantic.types import List


from api_tests.schemas.physical import Physical
from api_tests.schemas.owners import Owners

class DetailedInfo(BaseModel): #внутри этой шляпы лежат объекты поэтому делаем для них отдельные классы и указываем
    physical: Physical
    owners: List[Owners] #а здесь мы заимпортили дополнительно list, т.к. там list из ownerов
