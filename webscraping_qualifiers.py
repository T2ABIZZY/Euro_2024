from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import Functions
import re
import csv
import time
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

home_rank_headers = [
    'Expected goals(xG)', 'Total shots', 'Shots on target', 'Big chances',
    'Big chances missed', 'Accurate passes', 'Fouls committed', 'Corners',
    'Total shots.', 'Shots off target', 'Shots on target.', 'Blocked shots',
    'Hit woodwork', 'Shots inside box', 'Shots outside box', 'Expected goals (xG)',
    'xG open play', 'xG set play', 'Non-penalty xG', 'xG on target (xGOT)',
    'Passes', 'Accurate passes', 'Own half', 'Opposition half',
    'Accurate long balls', 'Accurate crosses', 'Throws', 'Touches in opposition box',
    'Offsides', 'Tackles won', 'Interceptions', 'Blocks',
    'Clearances', 'Keeper saves', 'Yellow cards', 'Red cards',
    'Duels won', 'Ground duels won', 'Aerial duels won', 'Successful dribbles'
]

away_rank_headers = [
    'Expected goals(xG)', 'Total shots', 'Shots on target', 'Big chances',
    'Big chances missed', 'Accurate passes', 'Fouls committed', 'Corners',
    'Total shots.', 'Shots off target', 'Shots on target.', 'Blocked shots',
    'Hit woodwork', 'Shots inside box', 'Shots outside box', 'Expected goals (xG)',
    'xG open play', 'xG set play', 'Non-penalty xG', 'xG on target (xGOT)',
    'Passes', 'Accurate passes', 'Own half', 'Opposition half',
    'Accurate long balls', 'Accurate crosses', 'Throws', 'Touches in opposition box',
    'Offsides', 'Tackles won', 'Interceptions', 'Blocks',
    'Clearances', 'Keeper saves', 'Yellow cards', 'Red cards',
    'Duels won', 'Ground duels won', 'Aerial duels won', 'Successful dribbles'
]
home_rank_dict = {header: [] for header in home_rank_headers}
away_rank_dict = {header: [] for header in away_rank_headers}

def fetch_data(soup):
    header = soup.find('div', 'css-1pf15hj-MFHeaderInfoBoxCSS')
    data['stadium'].append(clean_text(header.find('a','css-ndn9i5-VenueCSS').span.text))
    data['attendance'].append(header.find('div', 'css-1r6wxia-AttendanceCSS').span.text)
    main_board = soup.find('section','css-154n3ly-MFHeaderFullscreenSection')
    home = main_board.find('span','css-12r3z1-TeamName')
    data['home_team'].append(home.find('span').text)
    away = main_board.find('span','css-4nnvmn-TeamName')
    data['away_team'].append(away.find('span').text)
    score = main_board.find('span', 'css-ktw5ic-MFHeaderStatusScore').text
    data['home_goals'].append(score[0])
    data['away_goals'].append(score[-1])
    try:
        home_ranks = soup.find_all('div', class_='css-136hnlq-StatBox')
        away_ranks = soup.find_all('div',class_='css-1hkvumm-StatBox')
        if len(home_ranks) == len(home_rank_headers):
            for header, rank in zip(home_rank_headers, home_ranks):
                home_rank_dict[header].append(rank.get_text(strip=True))
            for header, rank in zip(away_rank_headers, away_ranks):
                away_rank_dict[header].append(rank.get_text(strip=True))
        else:
            print("Error: The number of home_ranks does not match the number of headers.")
    except Exception as e:
        print(f"An error occurredss: {e}")
    return data,home_rank_dict,away_rank_dict

def fetch_matches(driver):
    try:
        page_source = driver.page_source
        soup = BeautifulSoup(page_source, 'html.parser')
        matches = soup.select('div.slick-slide.slick-active a.css-hvo6tv-MatchWrapper')
        for match in matches:
            relative_link = match['href']
            full_link = f"https://www.fotmob.com{relative_link}:tab=stats"
            driver.get(full_link)
            element_present = EC.presence_of_all_elements_located((By.CLASS_NAME, 'css-136hnlq-StatBox'))
            WebDriverWait(driver, 10).until(element_present)
            element_present = EC.presence_of_all_elements_located((By.CLASS_NAME, 'css-1hkvumm-StatBox'))
            WebDriverWait(driver, 10).until(element_present)
            page_source = driver.page_source
            soup = BeautifulSoup(page_source, 'html.parser')
            fetch_data(soup)
    except Exception as e:
        print(f"An error occurreds: {e}")

def save_to_csv(data,home_rank_dict,away_rank_dict):
    with open("Euro_2024_Matches.csv",'w',newline='') as file:
        wr = csv.writer(file)
        wr.writerow([
            "stadium", "attendance", "home_team", "away_team", "home_goals", "away_goals",
            *['Home ' + header for header in home_rank_headers],
            *['Away ' + header for header in away_rank_headers]
        ])

        for i in range(len(data['stadium'])):
            row = [
                data['stadium'][i], data['attendance'][i], data['home_team'][i], data['away_team'][i],
                data['home_goals'][i], data['away_goals'][i],
                *[home_rank_dict[header][i] for header in home_rank_headers],
                *[away_rank_dict[header][i] for header in away_rank_headers]
            ]
            wr.writerow(row)
def main():
    start_time = time.time()
    original_link = "https://www.fotmob.com/leagues/50/matches/euro/by-round"
    driver = Functions.setup_driver()
    driver.get(original_link)

    try:
        rounds = ["Round 1", "Round 2", "Round 3", "Round of 16", "Quarter-final"]

        for round_name in rounds:
            which_round = Select(driver.find_element(By.CLASS_NAME, "css-hoemwv-Select"))
            which_round.select_by_visible_text(round_name)
            fetch_matches(driver)
            driver = Functions.setup_driver()
            driver.get(original_link)

        save_to_csv(data, home_rank_dict, away_rank_dict)
        print("--- %s seconds ---" % (time.time() - start_time))
    except Exception as e:
        print(f"an error occurred {e}")
    finally:
        driver.quit()


if __name__ == "__main__":
    main()
