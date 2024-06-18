from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
import Functions

def fetch_data(driver):
    try:

        page_source = driver.page_source
        soup = BeautifulSoup(page_source, 'html.parser')
        matches = soup.find_all('a', class_='css-13nvyko-MatchWrapper')
        for match in matches:
            relative_link = match['href']
            full_link = f"https://www.fotmob.com{relative_link}:tab=stats"
            driver.get(full_link)
            page_source = driver.page_source
            soup = BeautifulSoup(page_source, 'html.parser')


    except Exception as e:
        print(f"An error occurred: {e}")


def main():
    driver = Functions.setup_driver()
    driver.get("https://www.fotmob.com/leagues/50/matches/euro/by-round")
    try:
        which_round = Select(driver.find_element(By.CLASS_NAME, "css-1o54t4m-Select-applyMediumHover"))
        which_round.select_by_visible_text("Round 1")
        fetch_data(driver)
        print(a)
    except Exception as e:
        print(f"an error occurred {e}")
    finally:
        driver.quit()


if __name__ == "__main__":
    main()
