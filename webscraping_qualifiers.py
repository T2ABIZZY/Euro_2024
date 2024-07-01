from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.wait import WebDriverWait
import time
import Functions
import re
def clean_text(text):
    text = re.sub(r'[^a-zA-Z0-9\s]', '', text)
    text = text.strip()
    return text
def fetch_data(soup):
    header = soup.find('div', 'css-1pf15hj-MFHeaderInfoBoxCSS')
    date =[header.find('div','css-1tttqnj-MatchDateCSS').time['datetime']]
    stadium = [clean_text(header.find('a','css-ndn9i5-VenueCSS').span.text)]
    attendance = [header.find('div', 'css-1r6wxia-AttendanceCSS').span.text]


    print(attendance)
def fetch_matches(driver):
    try:
        page_source = driver.page_source
        soup = BeautifulSoup(page_source, 'html.parser')
        matches = soup.select('div.slick-slide.slick-active a.css-hvo6tv-MatchWrapper')
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
        which_round = Select(driver.find_element(By.CLASS_NAME, "css-f033xm-Select"))
        which_round.select_by_visible_text("Round 1")
        fetch_matches(driver)
        #Round 2
        driver = Functions.setup_driver()
        driver.get(original_link)
        which_round = Select(driver.find_element(By.CLASS_NAME, "css-f033xm-Select"))
        which_round.select_by_visible_text("Round 2")
        fetch_matches(driver)
    except Exception as e:
        print(f"an error occurred {e}")
    finally:
        driver.quit()


if __name__ == "__main__":
    main()
