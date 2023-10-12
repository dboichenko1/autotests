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

options = Options()
headless_bool = False
options.headless = headless_bool
browser = webdriver.Chrome(options=options)

browser.implicitly_wait(5)
beta = "https://beta.tradingview.com"
default_ws_host = {"stable":"dal2-stable-charts.xstaging.tv","testing":"dal2-adolgov-backend.xstaging.tv"}
default_ws_host_input = input(f'Исполльзовать дефолтные ws_host? y/n \n{default_ws_host} ')
if default_ws_host_input == "y":
    ws_host_dict = default_ws_host
else:
    ws_host_dict = {"stable":f'{input("Введите стейбловый лейаут в формате dal2-studies-1-backend.xstaging.tv ")}',"testing":f'{input("Введите тестовый лейаут в формате dal2-studies-2-backend.xstaging.tv ")}'}
layout_dict = {'basicstudies':['GNuvT7h0','zJlhAtff','lPS6jvVP','NzOOaaky'],'prostudies':['cLj969cv','mrhfAZWq','OXQkZfTO','zpFnYlQJ','ZR9K45TE','3AeJgcoK','zdBSTJLC','uuBtLNx6'],'corestudies':['bADrHwko']}
choose_case = input("Какой тест запускаем? Введите название пакета без tv-. Для запуска всех тестов введите all\n")
delete_identical_files = input("Удалять одинаковые файлы? (y/n) ")
difmod = "simple"


def check_exists_element(metod_search,data_sarch):
    try:
        browser.find_element(metod_search,data_sarch)
    except NoSuchElementException:
        return False
    return True

#login
def authorization():
    #простая авторизация под батутом 
    browser.get(beta)
    user_menu = browser.find_element(By.CSS_SELECTOR, 'button[aria-label="Open user menu"]').click()
    sign_in = browser.find_element(By.CSS_SELECTOR, 'button[role="menuitem"]').click()
    email_button = browser.find_element(By.CSS_SELECTOR, 'button[name="Email"]').click()
    email_input = browser.find_element(By.CSS_SELECTOR, 'input[id="id_username"]').send_keys("Batut") #Admin
    password_input = browser.find_element(By.CSS_SELECTOR, 'input[id="id_password"]').send_keys("1234") #dXeeuM4r
    button_sign_in_atorization = browser.find_element(By.XPATH, '//button[contains(@class,"submitButton")]').click()
    if check_exists_element(By.XPATH,'//*[text()="Please confirm that you are not a robot by clicking the captcha box."]'): #потом реализовать автопроход капчи
        input("Пройдите капчу и нажмите логин, введите любой текст для продолжения ")
    #записываем полученные куки
    session = browser.get_cookies()
    for cookie in session:
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
    time.sleep(1)
    #откатываемся к первой доступной дате:
    while check_exists_element(By.CSS_SELECTOR,'[aria-label="Go to"]') == False:
        time.sleep(1)
    go_to = browser.find_element(By.CSS_SELECTOR,'[aria-label="Go to"]').click()
    time.sleep(1)
    data_value = browser.find_element(By.CSS_SELECTOR,"[class='input-RUSovanF size-small-RUSovanF with-end-slot-RUSovanF']").get_attribute("value")
    if data_value != "1023-01-01":
        data = browser.find_element(By.CSS_SELECTOR,"[class='input-RUSovanF size-small-RUSovanF with-end-slot-RUSovanF']")
        actions = ActionChains(browser)
        for i in range(10):
            actions.send_keys_to_element(data, Keys.BACKSPACE).perform()
        data.send_keys("1023-01-01")
    time.sleep(2)
    submit_go_to = browser.find_element(By.CSS_SELECTOR,'[data-name="submit-button"]').click()
    time.sleep(10) #чтоб успели загрузиться все стадисы 
    saved_menu = browser.find_element(By.CSS_SELECTOR,'[data-name="save-load-menu"]').click()
    export_chart_data = browser.find_element(By.XPATH, '//*[text()="Export chart data…"]').click()
    chart_name = browser.find_element(By.XPATH,'//*[@id="chart-select"]/span[1]/span/span').text
    export_button = browser.find_element(By.XPATH,'//*[text()="Export"]').click()
    time.sleep(5) #чтоб успел скачаться файл

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
    for i in layout_dict['basicstudies']:
        # if i == "NzOOaaky":
        #     get_nonseries()
        export_data(i,ws_host_dict['stable'])
        export_data(i,ws_host_dict['testing'])
        basicstudies_result[i] = diff('basicstudies',i)
        if delete_identical_files == "y" and diff('basicstudies',i) : shutil.rmtree(f'testing_data/basicstudies/{i}', ignore_errors=True) 

    return basicstudies_result
def prostudies():
    '''
    возвращает словарь: ключи лейауты, значение - диф
    '''
    prostudies_result = {}
    for i in layout_dict['prostudies']:
        export_data(i,ws_host_dict['stable'])
        export_data(i,ws_host_dict['testing'])
        prostudies_result[i] = diff('prostudies',i)
        if delete_identical_files == "y" and diff('prostudies',i) : shutil.rmtree(f'testing_data/prostudies/{i}', ignore_errors=True) 

    return prostudies_result
def corestudies():
    '''
    возвращает словарь: ключи лейауты, значение - диф
    '''
    corestudies_result = {}
    for i in layout_dict['corestudies']:
        export_data(i,ws_host_dict['stable'])
        export_data(i,ws_host_dict['testing'])
        corestudies_result[i] = diff('corestudies',i)
        if delete_identical_files == "y" and diff('corestudies',i) : shutil.rmtree(f'testing_data/corestudies/{i}', ignore_errors=True)
 
    return corestudies_result
# start
def start():
    result = []
    authorization()
    if choose_case == "basicstudies":
        result.append(basicstudies())
    if choose_case == "prostudies":
        result.append(prostudies())
    if choose_case == "corestudies":
        result.append(corestudies())       
    print(result)
    if choose_case == "all":
        result.append(basicstudies())
        time.sleep(2)
        result.append(prostudies())
        time.sleep(2)
        result.append(corestudies())
    print(result)
    if input("Удалить директорию testing_data? (y/n) " ) == "y" : shutil.rmtree("testing_data", ignore_errors=True)
start()


#TO DO:
'''
diff() - create usability dff mode, search good library
def get_nonseries() - make connect to websocket and seach first du looks https://stackoverflow.com/questions/20907180/getting-console-log-output-from-chrome-with-selenium-python-api-bindings
'''
