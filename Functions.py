from bs4 import BeautifulSoup
import time
import csv
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service

def setup_driver():
    chrome_options = Options()
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument('--incognito')
    chrome_options.add_argument("--disable-dev-shm-usage")
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    return driver

def wait_for_element(driver, by, value, timeout=10):
    return WebDriverWait(driver, timeout).until(EC.element_to_be_clickable((by, value)))


def scroll_to_element(driver, element, scroll_pause_time=0.5):
    while True:
        driver.execute_script("window.scrollBy(0, 500);")
        time.sleep(scroll_pause_time)
        if driver.execute_script("return (window.innerHeight + window.scrollY) >= arguments[0].getBoundingClientRect().bottom;", element):
            driver.execute_script("arguments[0].scrollIntoView(true);", element)
            break
