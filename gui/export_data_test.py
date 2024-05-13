import time
from selenium import webdriver
from selenium.webdriver.common.by import By
import os
import shutil
import filecmp
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options
import pickle
import threading
import re
import multiprocessing
class Studilib():
    def __init__(self,config):
        self.stable = config["stable"]
        self.testing = config["testing"]
        self.layouts_export = config["packages_for_export_data"]
        self.delete_identical_files = config["delete_identical_files"]
        self.beta = config["beta"]
        self.cookies = pickle.load(open(config["cookies_path"], "rb"))
        self.export_test_result = {
            pack:[] for pack, layout_list in self.layouts_export.items()
        }
        self.nonseries_test_result = {}

    # Support functuion
    def check_exists_element(self,metod_search, data_sarch,browser):
        try:
            browser.find_element(metod_search, data_sarch)
        except NoSuchElementException:
            return False
        else:
            return True
    def export_data(self,layout, ws_host,browser):
        '''
        экспортирует данные с лейаута и сохраняет в папку с проектом
        '''
        browser.get(f'{self.beta}/chart/{layout}/?ws_host={ws_host}')
        # скрываем едитор чтоб был доступен го ту
        if self.check_exists_element(By.CSS_SELECTOR, '[aria-label="Collapse panel"]',browser):
            browser.find_element(By.CSS_SELECTOR, '[aria-label="Collapse panel"]').click()

        # принимаем куки
        if self.check_exists_element(By.CSS_SELECTOR, '[data-overflow-tooltip-text="Accept all "]',browser):
            browser.find_element(By.CSS_SELECTOR, '[data-overflow-tooltip-text="Accept all "]').click()

        while self.check_exists_element(By.XPATH, '//*[@data-status="loading"]',browser):  # любая загрузка стадиса
            time.sleep(1)
        # откатываемся к первой доступной дате:
        while not self.check_exists_element(By.CSS_SELECTOR, '[aria-label="Go to"]',browser):
            time.sleep(2)
        go_to = browser.find_element(By.CSS_SELECTOR, '[aria-label="Go to"]').click()
        data_value = browser.find_element(By.CSS_SELECTOR,"[class='input-RUSovanF size-small-RUSovanF with-end-slot-RUSovanF']").get_attribute("value")
        if data_value != "1023-01-01":
            data = browser.find_element(By.CSS_SELECTOR,"[class='input-RUSovanF size-small-RUSovanF with-end-slot-RUSovanF']")
            actions = ActionChains(browser)
            for i in range(10):
                actions.send_keys_to_element(data, Keys.BACKSPACE).perform()
            data.send_keys("1023-01-01")
        submit_go_to = browser.find_element(By.CSS_SELECTOR, '[data-name="submit-button"]').click()
        # это повторение действий нужно потому что на тяжелый лейаутах первый го ту не срабатывает и соответстветнно, експорт дата берется неверная
        for i in range(3):
            go_to
            submit_go_to
            while self.check_exists_element(By.XPATH, '//*[@data-status="loading"]',browser):  # любая загрузка стадиса
                time.sleep(1)
        saved_menu = browser.find_element(By.CSS_SELECTOR, '[data-name="save-load-menu"]').click()
        export_chart_data = browser.find_element(By.XPATH, '//*[text()="Export chart data…"]').click()
        chart_name = browser.find_element(By.XPATH, '//*[@id="chart-select"]/span[1]/span/span').text
        export_button = browser.find_element(By.XPATH, '//*[text()="Export"]').click()
        return chart_name

    def diff(self):
        for pack, layout_list in self.layouts_export.items():
            for layout in layout_list:
                idential = filecmp.cmp(
                    f"testing_data/{pack}/{layout}/stable.csv",
                    f"testing_data/{pack}/{layout}/testing.csv",
                     shallow = False
                )
                self.export_test_result[pack].append((layout,idential))
                if self.delete_identical_files and idential:
                    shutil.rmtree(f'testing_data/{pack}/{layout}', ignore_errors=True)
    def create_direcory(self):
        os.makedirs("testing_data")
        os.makedirs("source/stable")
        os.makedirs("source/testing")
        for key, value in self.layouts_export.items():
            os.makedirs(f'testing_data/{key}')
            for layout in value:
                os.makedirs(f'testing_data/{key}/{layout}')

    def init_and_autorization(self,env):
        options = Options()
        option_value = "headless"
        saving_dir = "source/stable" if env == self.stable else "source/testing"
        prefs = {"download.default_directory": saving_dir}
        options.add_argument(option_value)
        options.add_experimental_option("prefs", prefs)
        browser = webdriver.Chrome(options=options)
        browser.implicitly_wait(5)

        browser.get(self.beta)
        for cookie in self.cookies:
            browser.add_cookie(cookie)
        return (browser,saving_dir)
    def export_test_new(self,env):
        (browser,saving_dir) = self.init_and_autorization(env)
        for pack, layout_list in self.layouts_export.items():
            for layout in layout_list:
                #print(f'start {layout} in {pack}')
                chart_name = self.export_data(layout, env,browser)
                chart_name_patch = f'{chart_name.replace(":", "_").replace("*", "_").replace("/", "_")}.csv'
                while not os.path.exists(f'{saving_dir}/{chart_name_patch}'):time.sleep(1)
                shutil.move(f'{saving_dir}/{chart_name_patch}',
                            f'testing_data/{pack}/{layout}/{"stable" if env == self.stable else "testing"}.csv')

    def export_muliprocessing_start(self):
        t1 = threading.Thread(target=self.export_test_new, args=(self.stable,))
        t2 = threading.Thread(target=self.export_test_new, args=(self.testing,))
        t1.start()
        t2.start()
        t1.join()
        t2.join()

    def start(self):
        start = time.perf_counter()

        self.create_direcory()
        self.export_muliprocessing_start()
        self.diff()
        shutil.rmtree(f'source', ignore_errors=True)

        stop = time.perf_counter()

        print(self.export_test_result)
        print(f'{(stop-start)//60} m')
