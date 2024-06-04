from bs4 import BeautifulSoup
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
chrome_options = Options()
chrome_options.add_argument("--no-sandbox")  
chrome_options.add_argument("--disable-dev-shm-usage")  
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=chrome_options)
driver.get("https://inside.fifa.com/fifa-world-ranking/men")
accept_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, "onetrust-accept-btn-handler"))
    )
accept_button.click()
time.sleep(3)
driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CLASS_NAME,"button-module_contentContainer__QyE5V"))
    )
button.click()
time.sleep(10)
driver.quit()