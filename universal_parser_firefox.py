from typing import List, Tuple, Optional

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class WebsiteParser:
    # Путь к файлу geckodriver
    geckodriver_path = r'C:\Windows\System32\geckodriver.exe'
    def __init__(self, url: str):
        self.url = url
        options = Options()
        options.binary_location = r'C:\Program Files\Mozilla Firefox\firefox.exe'
        options.add_argument('--headless')
        options.add_argument('--disable-gpu')
        options.add_argument('--hide-scrollbars')
        self.driver = webdriver.Firefox(executable_path=self.geckodriver_path,options=options) # Укажите путь к GeckoDriver
    def __enter__(self):
        return self
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close_browser()
    def close_browser(self):
        self.driver.quit()
    def find_elements(self, selectors):
        """
        # Задаем селекторы для поиска элементов
        selectors = [
            {'by': 'tag', 'value': 'div'},        # Пример поиска по тегу
            {'by': 'class', 'value': 'my_class'}, # Пример поиска по классу
            {'by': 'id', 'value': 'my_id'},       # Пример поиска по идентификатору
            {'by': 'attr', 'value': '@data-id', 'attribute': 'data-id'}  # Пример поиска по атрибуту
        ]
        """
        self.driver.get(self.url)
        elements = []

        for selector in selectors:
            try:
                by, value = selector['by'], selector['value']
                if by == 'tag':
                    elements.extend(self.driver.find_elements(By.TAG_NAME, value))
                elif by == 'class':
                    elements.extend(self.driver.find_elements(By.CLASS_NAME, value))
                elif by == 'id':
                    elements.extend(self.driver.find_elements(By.ID, value))
                elif by == 'attr':
                    attribute = selector['attribute']
                    elements.extend([element.get_attribute(attribute) for element in self.driver.find_elements(By.XPATH, f'//*[@{value}]')])
                else:
                    raise ValueError(f"Неподдерживаемый тип селектора: {by}")

            except Exception as e:
                print(f"Ошибка при поиске элементов {value}: {e}")

        return elements
