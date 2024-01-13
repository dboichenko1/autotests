'''
аналогично вынесли из compute.py
'''

from pydantic import BaseModel, EmailStr
from pydantic.types import PaymentCardNumber
class Owners(BaseModel):
    name: str
    card_number: PaymentCardNumber #встроенный тип pydantic проверящий цифры на соответсвие алгоритму Луна
    email: EmailStr #встроенный валидатор emaila нужно будет поставить валидатион емейл библиотеку pip install pydantic[email]
