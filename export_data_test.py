import time 
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
import os
import shutil
import filecmp
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException 
from  selenium.webdriver.chrome.options import Options
import pickle
import re

options = Options()
option_value = "headless"
prefs = {"download.default_directory" : "."}
options.add_argument(option_value)
options.add_experimental_option("prefs",prefs)
browser = webdriver.Chrome(options=options)

browser.implicitly_wait(5)
beta = "https://beta.tradingview.com"
default_ws_host = {"stable":"dal2-studies-1-backend.xstaging.tv","testing":"dal2-studies-2-backend.xstaging.tv"}
default_ws_host_input = input(f'Исполльзовать дефолтные ws_host? y/n \n{default_ws_host} ')
if default_ws_host_input == "y":
    ws_host_dict = default_ws_host
else:
    ws_host_dict = {"stable":f'{input("Введите стейбловый лейаут в формате dal2-studies-1-backend.xstaging.tv ")}',"testing":f'{input("Введите тестовый лейаут в формате dal2-studies-2-backend.xstaging.tv ")}'}
layout_dict = {'basicstudies':['GNuvT7h0','zJlhAtff','lPS6jvVP','NzOOaaky'],'prostudies':['cLj969cv','mrhfAZWq','OXQkZfTO','zpFnYlQJ','ZR9K45TE','3AeJgcoK','zdBSTJLC','uuBtLNx6'],'corestudies':['bADrHwko']}
choose_case = input("Введите название тестируемого пакета, доступно: basicstudies, prostudies, corestudies.\nДля запуска всех тестов введите all\n")
delete_identical_files = input("Удалять одинаковые файлы? (y/n) ")
difmod = "simple"

#Вспомогательные функции

def timer(f):
    '''
    декоратор для замера времени. Время в секундах
    '''
    def ob():
        start = time.time()
        f()
        print("Время выполнения = " , time.time() - start)
    return(ob)

def check_exists_element(metod_search,data_sarch):
    try:
        browser.find_element(metod_search,data_sarch)
    except NoSuchElementException:
        return False
    return True

def current_testing_package(layout):
    '''
    Возвращает название текущего тестируемого пакета на основе лейаута
    '''
    current_testing_package = ""
    for key,value in layout_dict.items():
        for j in value:
            if j == layout:
                current_testing_package = key
    return current_testing_package
def current_testing_env(ws_host):
    '''
    Определеляет текущее тестовое окружение: стейбл или тестинг на основе ws_host
    '''
    current_testing_env = ""
    for key,value in ws_host_dict.items():
        if value == ws_host:
            current_testing_env = key
    return current_testing_env


#login
def authorization():
    #простая авторизация из куков под батутом
    browser.get(beta)

    cookies = pickle.load(open("cookies.pkl", "rb"))
    for cookie in cookies:
        browser.add_cookie(cookie)

#export data 
def export_data(layout,ws_host):
    '''
    экспортирует данные с лейаута и сохраняет в папку с проектом
    '''
    browser.get(f'{beta}/chart/{layout}/?ws_host={ws_host}')
    #скрываем едитор чтоб был доступен го ту 
    if check_exists_element(By.CSS_SELECTOR,'[aria-label="Hide panel"]'):
        browser.find_element(By.CSS_SELECTOR,'[aria-label="Hide panel"]').click()

    #принимаем куки
    if check_exists_element(By.CSS_SELECTOR,'[data-overflow-tooltip-text="Accept all"]'):
        browser.find_element(By.CSS_SELECTOR,'[data-overflow-tooltip-text="Accept all"]').click()
    while check_exists_element(By.CSS_SELECTOR,'[class="loader-l31H9iuA loader-_7n3rLPY"]'): #любая загрузка стадиса
        time.sleep(1)
    #откатываемся к первой доступной дате:
    while check_exists_element(By.CSS_SELECTOR,'[aria-label="Go to"]') == False:
        time.sleep(1)
    go_to = browser.find_element(By.CSS_SELECTOR,'[aria-label="Go to"]').click()
    data_value = browser.find_element(By.CSS_SELECTOR,"[class='input-RUSovanF size-small-RUSovanF with-end-slot-RUSovanF']").get_attribute("value")
    if data_value != "1023-01-01":
        data = browser.find_element(By.CSS_SELECTOR,"[class='input-RUSovanF size-small-RUSovanF with-end-slot-RUSovanF']")
        actions = ActionChains(browser)
        for i in range(10):
            actions.send_keys_to_element(data, Keys.BACKSPACE).perform()
        data.send_keys("1023-01-01")
    submit_go_to = browser.find_element(By.CSS_SELECTOR,'[data-name="submit-button"]').click()
    #эта повторение действий нужно потому что на тяжелый лейаутах первый го ту не срабатывает и соответстветнно, експорт дата берется неверная
    for i in range(3):
        go_to
        submit_go_to
        while check_exists_element(By.CSS_SELECTOR,'[class="loader-l31H9iuA loader-_7n3rLPY"]'): #любая загрузка стадиса
            time.sleep(1)
    saved_menu = browser.find_element(By.CSS_SELECTOR,'[data-name="save-load-menu"]').click()
    export_chart_data = browser.find_element(By.XPATH, '//*[text()="Export chart data…"]').click()
    chart_name = browser.find_element(By.XPATH,'//*[@id="chart-select"]/span[1]/span/span').text
    export_button = browser.find_element(By.XPATH,'//*[text()="Export"]').click()
    #ждем пока скачается файл
    while not os.path.exists(f'{chart_name.replace(":", "_").replace("*","_").replace("/","_")}.csv'):
        time.sleep(1)

    #создаем нужные папки по пакетам если их нет
    if not os.path.isdir(f'testing_data/{current_testing_package(layout)}/{layout}'):
        os.makedirs(f'testing_data/{current_testing_package(layout)}/{layout}')

    #Переносим експортированные данные из текущей директории в нужную папку и переименовываем
    shutil.move(f'{chart_name.replace(":", "_").replace("*","_").replace("/","_")}.csv',f'testing_data/{current_testing_package(layout)}/{layout}/{current_testing_env(ws_host)}.csv')  


#diff
def diff(current_testing_package,layout,nonseries = False,key = ""):
    '''
    в режиме симпл возвращает тру фолс по расхождениям в файлам
    в режиме dff возвращает дифф по файлам
    '''
    if difmod == "simple":
        if nonseries == False:
            return filecmp.cmp(f'testing_data/{current_testing_package}/{layout}/stable.csv', f'testing_data/{current_testing_package}/{layout}/testing.csv', shallow=False)
        if nonseries == True:
            return filecmp.cmp(f'testing_data/{current_testing_package}/{layout}_nonseries/{key}/stable.json', f'testing_data/{current_testing_package}/{layout}_nonseries/{key}/testing.json', shallow=False)
#get nonseries 
def get_nonseries(layout,ws_host):
    '''
    Создает в директории с тестируемым пакетом директории {layout}_nonseries, внутри отдельно директории с id-шниками, внутри которых файлы стейбл и тестинг json с первым дата апдейтом
    Возвращает массив с id-шниками
    '''
    browser.get(f'{beta}/chart/{layout}/?ws_host={ws_host}')
    #команда для логов включения
    browser.execute_script("lon(true)")
    time.sleep(10) #чтоб успели прийти все апдейты, через ожидание загрузки всех ожиданий стадисов почему то не работает, нонсерия не успевает приходить хз
    #команда для логов получения - возвращает массив с строками
    logs = browser.execute_script('return lget(1000000);')

    #собираю все дата апдейты и id-шники стадисов
    create_study_id_dict = {}
    all_du = []
    for str in logs:
        if "create_study" in str:
            create_study_id_dict[(re.search(r"st\d+",str).group())] = "" #вылавливаем id-шник create_study и конвертим из объекта re.Match в строку(group()) r перед строкой позволяет не учитывать экранирование
        elif "'m':'du'" in str: #'m':'du' потому что просто du дает неверный результат - был баг 
            all_du.append(str)
    # проходимся по всем записаным айдишникам(ключи) и ищем их в каждой строчке массива с дата апдейтам
    # все вхождения id-шника, пихаем в массив, далее проверяем что там нет левых ст11 12 и т.д. и берем из него самую большую строку и записываем как велью по ключу
    for key,value in create_study_id_dict.items():
        list_du_with_some_id = []
        for du in all_du:
            if key in du:
                list_du_with_some_id.append(du)
        if len(key) < 4: #отлавливаю st1 st2 и т.д. до 9
                for i in range(10):
                    for str in list_du_with_some_id: # прохожусь по каждой строке
                        if f"{key}{i}" in str: #проверю что для st1 st2 и т.д. до 9 не попали st11, st12 и т.д. если будут лейауты больше чем с 99 стадисами нужно будет поправить проверку
                            list_du_with_some_id.remove(str) # и удаляю их если они туда попали                
        if len(list_du_with_some_id) !=0: #на всякий случай, что все не сломалось если будет пустой массив
            create_study_id_dict[key]=re.sub("^.*'ns':","",max(list_du_with_some_id, key=len)).replace("\\'","'") #здесь я убираю лишнее и меняю кавычки (чтоб избежать дифа в каждом файле)
        else:
            print(f'В {current_testing_package(layout)}/{layout}_nonseries/{key}/{current_testing_env(ws_host)} не было дата апдейтов!!!')
    # из самой длинной строки массива, куда записал все вхождения по ключам с стдешниками, самая длинная строка = первый дата апдейт - т.к. больше всего весит - проверил.
    # Может быть позже придумаю как брать первый дата апдейт менее костыльно  

    #создаю внутри папки с лейаутом папки по каждому стадису и записываю туда первый дата апдейт в формате json
    for key,value in create_study_id_dict.items():
        if not os.path.isdir(f'testing_data/{current_testing_package(layout)}/{layout}_nonseries/{key}'):
            os.makedirs(f'testing_data/{current_testing_package(layout)}/{layout}_nonseries/{key}')

        with open(f"testing_data/{current_testing_package(layout)}/{layout}_nonseries/{key}/{current_testing_env(ws_host)}.json","w+") as q:
            q.write(f'{value}')
    return list(create_study_id_dict.keys())


#testcases

def basicstudies():
    '''
    возвращает словарь: ключи лейауты, значение - диф
    '''
    basicstudies_result = {}
    print("start basicstudies...")
    for i in layout_dict['basicstudies']:
        if i == "NzOOaaky": #это лейаут по которому нужно допом дифнуть нонсерию
            print(f'start nonseries test for {i}')
            key_id = get_nonseries(i,ws_host_dict['stable']) #создаем файловую структуру для стейбловый и сразу записываем массив айдишников, с тестингом они одинаковые (в рамках лейаута)
            get_nonseries(i,ws_host_dict['testing']) #и для тестовых 
            for id in key_id: 
                basicstudies_result[f'{i}_nonseries/{id}'] = diff('basicstudies',i,nonseries=True,key = id) #также делаем диф только по каждому айдишнику который накинут на чарт 
                if delete_identical_files == "y" and basicstudies_result[f'{i}_nonseries/{id}'] : shutil.rmtree(f'testing_data/basicstudies/{i}_nonseries/{id}', ignore_errors=True)
                print(f'стадис с id: {id} is ready! The files are identical: {basicstudies_result[f"{i}_nonseries/{id}"]}')
            print("nonseries test is ready!")
        export_data(i,ws_host_dict['stable'])
        export_data(i,ws_host_dict['testing'])
        basicstudies_result[i] = diff('basicstudies',i)
        if delete_identical_files == "y" and basicstudies_result[i] : shutil.rmtree(f'testing_data/basicstudies/{i}', ignore_errors=True)
        print(f'{i} is ready! The files are identical: {basicstudies_result[i]}')
    print("basicstudies is ready!")
    return basicstudies_result

def prostudies():
    '''
    возвращает словарь: ключи лейауты, значение - диф
    '''
    prostudies_result = {}
    print("start prostudies...")
    for i in layout_dict['prostudies']:
        export_data(i,ws_host_dict['stable'])
        export_data(i,ws_host_dict['testing'])
        prostudies_result[i] = diff('prostudies',i)
        if delete_identical_files == "y" and diff('prostudies',i) : shutil.rmtree(f'testing_data/prostudies/{i}', ignore_errors=True) 
        print(f'{i} is ready. The files are identical: {prostudies_result[i]}')
    print("prostudies is ready!")
    return prostudies_result

def corestudies():
    '''
    возвращает словарь: ключи лейауты, значение - диф
    '''
    corestudies_result = {}
    print("start corestudies...")
    for i in layout_dict['corestudies']:
        export_data(i,ws_host_dict['stable'])
        export_data(i,ws_host_dict['testing'])
        corestudies_result[i] = diff('corestudies',i)
        if delete_identical_files == "y" and diff('corestudies',i) : shutil.rmtree(f'testing_data/corestudies/{i}', ignore_errors=True)
        print(f'{i} is ready. The files are identical: {corestudies_result[i]}')
    print("corestudies is ready!")
    return corestudies_result
# start
@timer
def start():
    result = []
    authorization()
    if choose_case == "basicstudies":
        result.append({"basicstudies" : basicstudies()})
    if choose_case == "prostudies":
        result.append({"prostudies" : prostudies()})
    if choose_case == "corestudies":
        result.append({"corestudies" : corestudies()})      
    if choose_case == "all":
        result.append({"basicstudies" : basicstudies()})     
        result.append({"prostudies" : prostudies()})
        result.append({"corestudies" : corestudies()})    
    print(f'all right! result:')
    for i in result:
        for key,value in i.items():
            print(f'\n{key.upper()}')
            for k,v in value.items():
                print(f'{k} : {v}')
start()

if input("Удалить директорию testing_data? (y/n) " ) == "y" : shutil.rmtree("testing_data", ignore_errors=True)


#TO DO:
'''
diff() - create usability dff mode, search good library
make all in docker container
'''
#PROBLEB:
'''
1. проблема с получением дата апдейтов по 13+стадису, посмотреть в консоли браузера - дата апдейты есть , разобраться. Сейчас туда прилетают пустые дата апдейты. Попробовал сделать 6 стадисов на чарте, все равно упорно по 4 последним прилета..т пустые дата апдейты. Очено странно
дополнение: поведение этой функции очень непредсказуемо: те стшники которые загружаются только при прогоне этого лейаута возвращают пустой дата апдейт при прогоне нескольких леаутов.
Нужно разобраться что там не так - возможно проблема все таки на этапе получения логов. 
Самое простот что можно сделать - ели массив пустой - проверка уже есть по новой запрашивать логи и выполнять все заново.
2. полученные файлы не распаршиваются в json, посмотреть что еще нужно убрать/заменить и использовать json дамп или лоад или что-то другое чтоб они сразу записывались в человеко читаемом виде 
3. Добавить лейауты вольбм профиля сюда и паттернов тож можно 
'''