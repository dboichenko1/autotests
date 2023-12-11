import math
stavka_yandex = 11

def calculator(stavka,kapital,srok,procent_every_day = False):
    '''
    srok in mounth
    '''
    result_kapital = kapital
    if procent_every_day:
        stavka_day = stavka/100/365
        srok_day = srok * 30.5
        for day in range(math.ceil(srok_day)):
            result_kapital += result_kapital * stavka_day
    else:
        stavka_mounth = stavka/100/12
        for mounth in range(srok):
            result_kapital += result_kapital * stavka_mounth
    return math.ceil(result_kapital - kapital)

yandex = calculator(11,50000,6,True)

alfa = calculator(11,50000,6)

ozon = calculator(13.9,50000,6)

print(f'yandex = {yandex}\nalfa = {alfa}\nozon = {ozon}')

