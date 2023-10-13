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
choose_case = input("Какой тест запускаем? Введите название пакета без tv-. Для запуска всех тестов введите all\n")
delete_identical_files = input("Удалять одинаковые файлы? (y/n) ")
difmod = "simple"

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
    #перенос сохраненного файла из  Download в папку с проектом/testing_data/имя тестируемого пакета/имя лейаута/stable.scv или testing.csv
    if not os.path.isdir('testing_data'):
        os.makedirs('testing_data')

    #определение текущего текстируемого пакета:
    current_testing_package = ""
    for key,value in layout_dict.items():
        for j in value:
            if j == layout:
                current_testing_package = key   

    if not os.path.isdir(f'testing_data/{current_testing_package}/{layout}'):
        os.makedirs(f'testing_data/{current_testing_package}/{layout}')

    #определение текущего окружения - стейбл или тестинг:
    current_testing_env = ""
    for key,value in ws_host_dict.items():
        if value == ws_host:
            current_testing_env = key
    if option_value == "headless": #это нужно потому что в этом режиме файлы сохраняются в текущую директорию, а без него в Downloads
        shutil.move(f'{chart_name.replace(":", "_").replace("*","_").replace("/","_")}.csv',f'testing_data/{current_testing_package}/{layout}/{current_testing_env}.csv')  
    else:
        shutil.move(f'/home/{os.getlogin()}/Downloads/{chart_name.replace(":", "_").replace("*","_").replace("/","_")}.csv',f'testing_data/{current_testing_package}/{layout}/{current_testing_env}.csv')  

#diff
def diff(current_testing_package,layout):
    '''
    в режиме симпл возвращает тру фолс по расхождениям в файлам
    в режиме dff возвращает дифф по файлам
    '''
    if difmod == "simple":
        return filecmp.cmp(f'testing_data/{current_testing_package}/{layout}/stable.csv', f'testing_data/{current_testing_package}/{layout}/testing.csv', shallow=False)

#get nonseries 
def get_nonseries():
    '''
    для получения нонсерии (лейаут NzOOaaky - потом добавить в значения basicstudies)
    по итогу лучше всего сделать так:
      кидаем в консоль лон тру 
      коннектимся к вебсокету
      грепаем первый дата апдейт
      посмотреть функцию get_log, типо того https://stackoverflow.com/questions/20907180/getting-console-log-output-from-chrome-with-selenium-python-api-bindings
    '''
    pass


#testcases

def basicstudies():
    '''
    возвращает словарь: ключи лейауты, значение - диф
    '''
    basicstudies_result = {}
    print("start basicstudies...")
    for i in layout_dict['basicstudies']:
        # if i == "NzOOaaky":
        #     get_nonseries()
        export_data(i,ws_host_dict['stable'])
        export_data(i,ws_host_dict['testing'])
        basicstudies_result[i] = diff('basicstudies',i)
        if delete_identical_files == "y" and diff('basicstudies',i) : shutil.rmtree(f'testing_data/basicstudies/{i}', ignore_errors=True)
        print(f'{i} is ready! The files are identical: {basicstudies_result[i]:}')
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
    print(f'all right! result:\n{result}')
start()
if input("Удалить директорию testing_data? (y/n) " ) == "y" : shutil.rmtree("testing_data", ignore_errors=True)


#TO DO:
'''
diff() - create usability dff mode, search good library
def get_nonseries() - make connect to websocket and seach first du looks https://stackoverflow.com/questions/20907180/getting-console-log-output-from-chrome-with-selenium-python-api-bindings
make all in docker container
'''
