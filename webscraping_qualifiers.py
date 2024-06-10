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

def main():
        driver = setup_driver()
if __name__ = "__main__":
    main()
