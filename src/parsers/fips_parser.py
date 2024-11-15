import sys

from undetected_chromedriver import Chrome, ChromeOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException
from fake_useragent import UserAgent

from ..constants import WEBDRIVER_WAIT_TIME


class FipsParser:
    def __init__(self):
        user_agent = UserAgent()
        options = ChromeOptions()
        options.add_argument("--enable-aggressive-domstorage-flushing")
        options.add_argument(f"--user-agent={user_agent.random}")
        options.add_argument("--headless=new")
        self.__driver = Chrome(options=options)
        self.__wait = WebDriverWait(self.__driver, WEBDRIVER_WAIT_TIME)

    def parse_by_query(self, query):
        self.__driver.get("https://www.fips.ru/iiss/db.xhtml")

        self.__click_on_element(
            By.XPATH, '//div[contains(text(), "Патентные документы РФ")]'
        )
        self.__click_on_element(By.XPATH, '//input[@value="выделить все"]')
        self.__click_on_element(By.XPATH, '//input[@value="перейти к поиску"]')

        search_input = self.__driver.find_element(
            By.XPATH, '//div[@class="input"]//textarea'
        )
        search_input.send_keys(query)
        self.__click_on_element(By.XPATH, '//input[@value="Поиск"]')

        patent_numbers = set(
            [
                url.text
                for url in self.__driver.find_elements(
                    By.XPATH, '//div[@class="td"][2]'
                )
            ]
        )
        url_text_map = {}

        for patent_number in patent_numbers:
            url_text_map[
                f"https://new.fips.ru/registers-doc-view/fips_servlet?DB=RUPAT&DocNumber={patent_number}&TypeFile=html"
            ] = self.__driver.execute_script("return document.body.innerText;")

        return url_text_map

    def __click_on_element(self, by, value):
        while True:
            try:
                self.__wait.until(EC.element_to_be_clickable((by, value))).click()
                break
            except StaleElementReferenceException:
                pass

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.__driver.quit()

    def _sigint_handler(self, signal_received, frame):
        self.__exit__(None, None, None)
        sys.exit(0)
