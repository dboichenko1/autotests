from selenium import webdriver
from  selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException 
import time
import pickle
import json
import re

option_value = "headless"
options = Options()
options.add_argument(option_value)

browser = webdriver.Chrome(options=options)

#ошибки
def check_exists_element(metod_search,data_sarch):
    try:
        browser.find_element(metod_search,data_sarch)
    except NoSuchElementException:
        return False
    return True
#куки
browser.get("https://beta.tradingview.com")
cookies = pickle.load(open("cookies.pkl", "rb"))
for cookie in cookies:
    browser.add_cookie(cookie)

browser.get("https://beta.tradingview.com/chart/NzOOaaky")
#команда для логов включения
browser.execute_script("lon(true)")
time.sleep(10) #чтоб успели прийти все апдейты
#команда для логов получения - возвращает массив с строками - если несколько стадисов не сработает 
logs = browser.execute_script('return lget(1000000);')
#берем самыую большую строку 
# longest_string = max(logs, key=len)
# new_string = re.sub("^.*ChartApi\.ChartSession:recv: ", "", longest_string)
create_study_dict = {}
for i in logs:
    if "create_study" in i:
        create_study_dict[(re.search(r"st\d+",i).group())] = "" #вылавливаем номер стадиса при создании и конвертим из объекта re.Match в строку с помощью group() r перед строкой позволяет не учитывать экранирование
        #print(i)

# проходимся по всем записаным ключам и ищем их в каждой строчке массива с логами все вхождения пихаем в массив, берем из него самую большую строку и записываем как велью по ключу - ст ЕСТЬ БАГ ВМЕСТО 1 ЗАПИСАЛСЯ 12 ВИДИМО ПОТОМУ ЧТО У НЕГО ДЛИНА БОЛЬШЕ, НУЖНО СДЕЛАТЬ СТРОГОЕ ВХОЖДЕНИЕ ПО 1 ДОЛЖЕН НАХОДИТЬ ТОЛЬКО СТ1
for k,v in create_study_dict.items():
    array_with_all_std = []
    for j in logs:
        if k in j:
            if "du" in j:
                if k == "st1":
                    if "st11" in j or "st12" in j: #жесткий костыль, чтоб в ст1 не попадал ст11 и ст12, надо придумать что-то другое + аналогично для ст1n ст2n ....
                        continue
                array_with_all_std.append(j)
    if len(array_with_all_std) !=0:
        create_study_dict[k]=re.sub("^.*ChartSession:recv: ","",max(array_with_all_std, key=len)) #здесь я убираю часть с временем (чтоб избежать дифа в каждом файле)
    # из самой длинной строки массива, куда записал все вхождения по ключам с стдешниками, самая длинная строка = первый дата апдейт - т.к. больше всего весит - проверил.
    # Может быть позже придумаю как брать первый дата апдейт менее костыльно  
        



# print(create_study_dict)

with open("result.txt","w+") as q:
    for k,v in create_study_dict.items():
        q.write(f'{k}:{v}\n\n')

# a = new_string
# print(type(a))
# #удаляем из нее лишнее и в json преобразуем
# with open("result.txt","w+") as q:
#     q.write(new_string)
# # for i in logs:
# #     if "'m':'du'" in i: 
# #         print(i)


