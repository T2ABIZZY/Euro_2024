import select

from bs4 import BeautifulSoup
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
import Functions

def main():
    driver = Functions.setup_driver()
    driver.get("https://www.fotmob.com/leagues/50/matches/euro/by-round")
    try:
        which_round = Select(driver.find_element(By.CLASS_NAME, "css-1o54t4m-Select-applyMediumHover"))
        which_round.select_by_visible_text("Round 1")

    except Exception as e:
        print(f"an error occurred {e}")
    finally:
        driver.quit()


if __name__ == "__main__":
    main()
