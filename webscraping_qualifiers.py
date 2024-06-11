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
import Functions

def fetch_scores(driver):
    page_source = driver.page_source
    soup = BeautifulSoup(page_source, 'html.parser')
    matches = soup.find_all('div', class_="event__match event__match--withRowLink event__"
                                          "match--static event__match--twoLine")
    home_team = [match.find('span', '_simpleText_zfz11_4 _webTypeSimpleText01_zfz11_8 _name_x6lwl_17').text for match in matches]
    print(home_team)
def main():
    driver = Functions.setup_driver()
    driver.get("https://www.flashscore.com/football/europe/euro/results/")
    try:
        cockies_button = Functions.wait_for_element(driver, By.ID, "onetrust-accept-btn-handler")
        cockies_button.click()
        time.sleep(3)
        show_more_button = Functions.wait_for_element(driver, By.CLASS_NAME, "event__more--static")
        Functions.scroll_to_element(driver, show_more_button)
        show_more_button.click()
        Functions.scroll_to_element(driver, show_more_button)
        show_more_button.click()
        fetch_scores(driver)
    except Exception as e:
        print(f"an error occurred {e}")
    finally:
        driver.quit()


if __name__ == "__main__":
    main()
