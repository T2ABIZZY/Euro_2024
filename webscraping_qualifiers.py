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
data={
    'stadium':[],
    'attendance':[],
    'home_team':[],
    'away_team':[],
    'home_goals':[],
    'away_goals':[]
}
rank_headers=[
    'Expected goals (xG)','Total shots','Shots on target','Big chances',
    'Big chances missed','Accurate passes','Fouls committed','Corners',
    'Total shots','Shots off target','Shots on target','Blocked shots'
    'Hit woodwork','Shots inside box','Shots outside box','Expected goals (xG)'
    'xG open play','xG set play','Non-penalty xG','xG on target (xGOT)'
    'Passes','Accurate passes','Own half','Opposition half'
    'Accurate long balls','Accurate crosses','Throws','Touches in opposition box'
    'Offsides','Tackles won','Interceptions','Blocks'
    'Clearances','Keeper saves','Yellow cards','Red cards'
    'Duels won','Ground duels won','Aerial duels won','Successful dribbles'
]
rank_data = {header: [] for header in rank_headers}
def fetch_data(soup):
    header = soup.find('div', 'css-1pf15hj-MFHeaderInfoBoxCSS')
    data['stadium'].append(clean_text(header.find('a','css-ndn9i5-VenueCSS').span.text))
    data['attendance'].append(header.find('div', 'css-1r6wxia-AttendanceCSS').span.text)
    main_board = soup.find('section','css-154n3ly-MFHeaderFullscreenSection')
    data['home_team'].append(main_board.find('div', 'css-1o6li2i-TeamMarkup').find('span',
                               'css-dpbuul-TeamNameItself-TeamNameOnTabletUp').text)
    data['away_team'].append(main_board.find('div', 'css-6p9nys-TeamMarkup').find('span',
                               'css-dpbuul-TeamNameItself-TeamNameOnTabletUp').text)
    score = main_board.find('span', 'css-ktw5ic-MFHeaderStatusScore').text
    data['home_goals'].append(score[0])
    data['away_goals'].append(score[-1])
    ranks = soup.find_all('div', class_='css-136hnlq-StatBox')

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
        which_round = Select(driver.find_element(By.CLASS_NAME, "css-1ugcbd1-Select"))
        which_round.select_by_visible_text("Round 1")
        fetch_matches(driver)
        #Round 2
        driver = Functions.setup_driver()
        driver.get(original_link)
        which_round = Select(driver.find_element(By.CLASS_NAME, "css-1ugcbd1-Select"))
        which_round.select_by_visible_text("Round 2")
        fetch_matches(driver)
        print(len(data['home_team']))
    except Exception as e:
        print(f"an error occurred {e}")
    finally:
        driver.quit()


if __name__ == "__main__":
    main()
