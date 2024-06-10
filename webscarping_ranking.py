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


def is_target_element_present(driver):
    elements = driver.find_elements(By.CLASS_NAME, "rank-cell_rank__yNDOI")
    return any(element.text== "210" for element in elements)
    

def fetch_ranking_data(driver):
    page_source = driver.page_source
    soup = BeautifulSoup(page_source, 'html.parser')
    ranks = soup.find_all('tr',
        class_="table-row-module_row__3wRGf table-row-module_hover__MdRZU table-row-module_regular__tAYiC data-grid-module_pointer"
               "__uipYu "
               "base-world-ranking-table_tableRow__fC_zY"
        )
    full_name_ranking= [rank.find('a','link-module_link__F9IVG team-cell_teamName__tyiAD').text for rank in ranks]
    small_name_ranking= [rank.find('a','link-module_link__F9IVG team-cell_teamCode__Yi4NC').text for rank in ranks]
    total_points=[rank.find('span','total-points-cell_points__JPjv3').text for rank in ranks]
    print(len(full_name_ranking))
    return full_name_ranking,small_name_ranking,total_points

def save_to_csv(full_name_ranking, small_name_ranking, total_points):
    with open("World_Ranking.csv",'w',newline='') as file:
        wr = csv.writer(file)
        wr.writerow(["Country","Abbreviations","Points"])
        for i in range(len(full_name_ranking)):
            wr.writerow([full_name_ranking[i],small_name_ranking[i],total_points[i]])
def main():
    driver = setup_driver()
    driver.get("https://inside.fifa.com/fifa-world-ranking/men")
    try:
        accept_button= wait_for_element(driver,By.ID,"onetrust-accept-btn-handler")
        accept_button.click()
        time.sleep(3)
        target_button = wait_for_element(driver,By.CLASS_NAME,"button-module_contentContainer__QyE5V")
        scroll_to_element(driver,target_button)
        driver.execute_script("arguments[0].click();", target_button)
        scroll_pause_time = 0.5
        while not is_target_element_present(driver):
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(scroll_pause_time)

        full_name_ranking,small_name_ranking, total_points= fetch_ranking_data(driver)
        save_to_csv(full_name_ranking,small_name_ranking,total_points)
    except Exception as e:
        print(f"an error occurred:{e}")
    finally:
        driver.quit()
if __name__ == "__main__":
    main()