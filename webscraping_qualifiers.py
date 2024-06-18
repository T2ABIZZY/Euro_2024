from bs4 import BeautifulSoup
import time
from selenium.webdriver.common.by import By
import Functions

def main():
    driver = Functions.setup_driver()
    driver.get("https://www.fotmob.com/leagues/50/matches/euro/by-round")
    try:
        time.sleep(5)

    except Exception as e:
        print(f"an error occurred {e}")
    finally:
        driver.quit()


if __name__ == "__main__":
    main()
