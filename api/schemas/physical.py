'''
вынесем сюда внутренний объект с Physical из compute для дальнешего переиспользования
'''

from pydantic import BaseModel,HttpUrl,UUID4
from pydantic.color import Color

class Physical(BaseModel):
    color: Color #валидация на пайлентиковский колор
    photo: HttpUrl #валидация на валидный тип http
    uuid: UUID4 #валидируем также через встроенный, там много разных, этот самый часто используемый