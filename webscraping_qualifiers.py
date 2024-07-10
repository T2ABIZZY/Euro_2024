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
        wr.writerow(["stadium","attendance","home_team",'away_team','home_goals','away_goals',
    'Home Expected goals(xG)','Home Total shots','Home Shots on target','Home Big chances',
    'Home Big chances missed','Home Accurate passes','Home Fouls committed','Home Corners',
    'Home Total shots.','Home Shots off target','Home Shots on target.','Home Blocked shots',
    'Home Hit woodwork','Home Shots inside box','Home Shots outside box','Home Expected goals (xG)',
    'Home xG open play','Home xG set play','Home Non-penalty xG','Home xG on target (xGOT)',
    'Home Passes','Home Accurate passes','Home Own half','Home Opposition half',
    'Home Accurate long balls','Home Accurate crosses','Home Throws','Home Touches in opposition box',
    'Home Offsides','Home Tackles won','Home Interceptions','Home Blocks',
    'Home Clearances','Home Keeper saves','Home Yellow cards','Home Red cards',
    'Home Duels won','Home Ground duels won','Home Aerial duels won','Home Successful dribbles',
    'Away Expected goals(xG)', 'Away Total shots', 'Away Shots on target.', 'Away Big chances',
    'Away Big chances missed', 'Away Accurate passes', 'Away Fouls committed', 'Away Corners',
    'Away Total shots.', 'Away Shots off target', 'Away Shots on target.', 'Away Blocked shots',
    'Away Hit woodwork', 'Away Shots inside box', 'Away Shots outside box', 'Away Expected goals (xG)',
    'Away xG open play', 'Away xG set play', 'Away Non-penalty xG', 'Away xG on target (xGOT)',
    'Away Passes', 'Away Accurate passes', 'Away Own half', 'Away Opposition half',
    'Away Accurate long balls', 'Away Accurate crosses', 'Away Throws',
    'Away Touches in opposition box',
    'Away Offsides', 'Away Tackles won', 'Away Interceptions', 'Away Blocks',
    'Away Clearances', 'Away Keeper saves', 'Away Yellow cards', 'Away Red cards',
    'Away Duels won', 'Away Ground duels won', 'Away Aerial duels won', 'Away Successful dribbles'
                     ])
        for i in range(len(data['stadium'])):
            row = [
                data['stadium'][i], data['attendance'][i], data['home_team'][i], data['away_team'][i],
                data['home_goals'][i], data['away_goals'][i],
                home_rank_dict['Expected goals(xG)'][i], home_rank_dict['Total shots'][i], home_rank_dict['Shots on target'][i],
                home_rank_dict['Big chances'][i],
                home_rank_dict['Big chances missed'][i], home_rank_dict['Accurate passes'][i], home_rank_dict['Fouls committed'][i],
                home_rank_dict['Corners'][i],
                home_rank_dict['Total shots'][i], home_rank_dict['Shots off target'][i], home_rank_dict['Shots on target'][i],
                home_rank_dict['Blocked shots'][i],
                home_rank_dict['Hit woodwork'][i], home_rank_dict['Shots inside box'][i], home_rank_dict['Shots outside box'][i],
                home_rank_dict['Expected goals (xG)'][i],
                home_rank_dict['xG open play'][i], home_rank_dict['xG set play'][i], home_rank_dict['Non-penalty xG'][i],
                home_rank_dict['xG on target (xGOT)'][i],
                home_rank_dict['Passes'][i], home_rank_dict['Accurate passes'][i], home_rank_dict['Own half'][i],
                home_rank_dict['Opposition half'][i],
                home_rank_dict['Accurate long balls'][i], home_rank_dict['Accurate crosses'][i], home_rank_dict['Throws'][i],
                home_rank_dict['Touches in opposition box'][i],
                home_rank_dict['Offsides'][i], home_rank_dict['Tackles won'][i], home_rank_dict['Interceptions'][i],
                home_rank_dict['Blocks'][i],
                home_rank_dict['Clearances'][i], home_rank_dict['Keeper saves'][i], home_rank_dict['Yellow cards'][i],
                home_rank_dict['Red cards'][i],
                home_rank_dict['Duels won'][i], home_rank_dict['Ground duels won'][i], home_rank_dict['Aerial duels won'][i],
                home_rank_dict['Successful dribbles'][i],away_rank_dict['Expected goals(xG)'][i], away_rank_dict['Total shots'][i], away_rank_dict['Shots on target'][i],
                away_rank_dict['Big chances'][i],
                away_rank_dict['Big chances missed'][i], away_rank_dict['Accurate passes'][i], away_rank_dict['Fouls committed'][i],
                away_rank_dict['Corners'][i],
                away_rank_dict['Total shots'][i], away_rank_dict['Shots off target'][i], away_rank_dict['Shots on target'][i],
                away_rank_dict['Blocked shots'][i],
                away_rank_dict['Hit woodwork'][i], away_rank_dict['Shots inside box'][i], away_rank_dict['Shots outside box'][i],
                away_rank_dict['Expected goals (xG)'][i],
                away_rank_dict['xG open play'][i], away_rank_dict['xG set play'][i], away_rank_dict['Non-penalty xG'][i],
                away_rank_dict['xG on target (xGOT)'][i],
                away_rank_dict['Passes'][i], away_rank_dict['Accurate passes'][i], away_rank_dict['Own half'][i],
                away_rank_dict['Opposition half'][i],
                away_rank_dict['Accurate long balls'][i], away_rank_dict['Accurate crosses'][i], away_rank_dict['Throws'][i],
                away_rank_dict['Touches in opposition box'][i],
                away_rank_dict['Offsides'][i], away_rank_dict['Tackles won'][i], away_rank_dict['Interceptions'][i],
                away_rank_dict['Blocks'][i],
                away_rank_dict['Clearances'][i], away_rank_dict['Keeper saves'][i], away_rank_dict['Yellow cards'][i],
                away_rank_dict['Red cards'][i],
                away_rank_dict['Duels won'][i], away_rank_dict['Ground duels won'][i], away_rank_dict['Aerial duels won'][i],
                away_rank_dict['Successful dribbles'][i]

            ]
            wr.writerow(row)
def main():
    original_link = "https://www.fotmob.com/leagues/50/matches/euro/by-round"
    driver = Functions.setup_driver()
    driver.get(original_link)
    try:
        start_time =time.time()
        # Round 1
        which_round = Select(driver.find_element(By.CLASS_NAME, "css-hoemwv-Select"))
        which_round.select_by_visible_text("Round 1")
        fetch_matches(driver)
        # #Round 2
        driver = Functions.setup_driver()
        driver.get(original_link)
        which_round = Select(driver.find_element(By.CLASS_NAME, "css-hoemwv-Select"))
        which_round.select_by_visible_text("Round 2")
        fetch_matches(driver)
        #Round 3
        driver = Functions.setup_driver()
        driver.get(original_link)
        which_round = Select(driver.find_element(By.CLASS_NAME, "css-hoemwv-Select"))
        which_round.select_by_visible_text("Round 3")
        fetch_matches(driver)
        # Round 16
        driver = Functions.setup_driver()
        driver.get(original_link)
        which_round = Select(driver.find_element(By.CLASS_NAME, "css-hoemwv-Select"))
        which_round.select_by_visible_text("Round of 16")
        fetch_matches(driver)
        #Quarter-final
        driver = Functions.setup_driver()
        driver.get(original_link)
        which_round = Select(driver.find_element(By.CLASS_NAME, "css-hoemwv-Select"))
        which_round.select_by_visible_text("Quarter-final")
        fetch_matches(driver)
        save_to_csv(data,home_rank_dict,away_rank_dict)
        print("--- %s seconds ---" % (time.time() - start_time))
    except Exception as e:
        print(f"an error occurred {e}")
    finally:
        driver.quit()


if __name__ == "__main__":
    main()
