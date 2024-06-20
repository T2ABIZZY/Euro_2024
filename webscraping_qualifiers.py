from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.wait import WebDriverWait
import time
import Functions
def fetch_data(soup):
    print("test")
def fetch_matches(driver):
    try:
        page_source = driver.page_source
        soup = BeautifulSoup(page_source, 'html.parser')
        matches = soup.select('div.slick-slide.slick-active a.css-9on8f0-MatchWrapper')
        print(matches)
        for match in matches:
            relative_link = match['href']
            full_link = f"https://www.fotmob.com{relative_link}:tab=stats"
            driver.get(full_link)
            page_source = driver.page_source
            soup = BeautifulSoup(page_source, 'html.parser')
            fetch_data(soup)
    except Exception as e:
        print(f"An error occurred: {e}")


def main():
    original_link = "https://www.fotmob.com/leagues/50/matches/euro/by-round"
    driver = Functions.setup_driver()
    driver.get(original_link)
    try:
        # Round 1
        which_round = Select(driver.find_element(By.CLASS_NAME, "css-9n0p7i-Select"))
        which_round.select_by_visible_text("Round 1")
        fetch_matches(driver)
        #Round 2
        driver = Functions.setup_driver()
        driver.get(original_link)
        which_round = Select(driver.find_element(By.CLASS_NAME, "css-9n0p7i-Select"))
        which_round.select_by_visible_text("Round 2")
        fetch_matches(driver)
    except Exception as e:
        print(f"an error occurred {e}")
    finally:
        driver.quit()


if __name__ == "__main__":
    main()
