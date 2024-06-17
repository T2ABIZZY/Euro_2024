from bs4 import BeautifulSoup
import time
from selenium.webdriver.common.by import By
import Functions

def main():
    driver = Functions.setup_driver()
    driver.get("https://www.eurosport.com/football/euro-qualifying/2024/calendar-results.shtml")
    try:
        print("testing")
    except Exception as e:
        print(f"an error occurred {e}")
    finally:
        driver.quit()


if __name__ == "__main__":
    main()
