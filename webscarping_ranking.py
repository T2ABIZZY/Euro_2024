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
chrome_options.add_argument('--incognito')
chrome_options.add_argument("--disable-dev-shm-usage")  
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=chrome_options)
driver.get("https://inside.fifa.com/fifa-world-ranking/men")
accept_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, "onetrust-accept-btn-handler"))
    )
accept_button.click()
time.sleep(3)

def is_element_in_view(driver, element):
    return driver.execute_script("return (window.innerHeight + window.scrollY) >= arguments[0].getBoundingClientRect().bottom;", element)

# Find the target button element
target = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.CLASS_NAME, "button-module_contentContainer__QyE5V"))
)

# Scroll incrementally until the target element is in view
scroll_pause_time = 0.5  # Time to wait between scrolls

while True:

    driver.execute_script("window.scrollBy(0, 500);")
    time.sleep(scroll_pause_time)

    if is_element_in_view(driver, target):
        driver.execute_script("arguments[0].scrollIntoView(true);", target)
        break

target = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.CLASS_NAME, "button-module_contentContainer__QyE5V"))
)

def is_target_element_present(driver):
    elements = driver.find_elements(By.CLASS_NAME, "rank-cell_rank__yNDOI")
    for element in elements:
        if element.text == "210":
            return True
    return False
    
driver.execute_script("arguments[0].click();", target)
while True:
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(scroll_pause_time)
    if is_target_element_present(driver):
        break


page_source = driver.page_source
soup = BeautifulSoup(page_source, 'html.parser')
ranking=[]
a=0
ranks = soup.find_all('tr',class_="table-row-module_row__3wRGf table-row-module_hover__MdRZU table-row-module_regular__tAYiC data-grid-module_pointer__uipYu base-world-ranking-table_tableRow__fC_zY")
for rank in ranks:
    print(rank.find('a','link-module_link__F9IVG team-cell_teamName__tyiAD').text)
    a=a+1
    if a==3:
        break
driver.quit()