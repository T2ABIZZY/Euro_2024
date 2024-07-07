from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import Functions
import re
import csv
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
    'Total shots','Shots off target','Shots on target','Blocked shots',
    'Hit woodwork','Shots inside box','Shots outside box','Expected goals (xG)',
    'xG open play','xG set play','Non-penalty xG','xG on target (xGOT)',
    'Passes','Accurate passes','Own half','Opposition half',
    'Accurate long balls','Accurate crosses','Throws','Touches in opposition box',
    'Offsides','Tackles won','Interceptions','Blocks',
    'Clearances','Keeper saves','Yellow cards','Red cards',
    'Duels won','Ground duels won','Aerial duels won','Successful dribbles'
]
rank_dict = {header: [] for header in rank_headers}
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

    if len(ranks) == len(rank_headers):
        for header, rank in zip(rank_headers, ranks):
            rank_dict[header].append(rank.get_text(strip=True))
    else:
        print("Error: The number of ranks does not match the number of headers.")
    print(len(ranks))
    return data,rank_dict

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
            page_source = driver.page_source
            soup = BeautifulSoup(page_source, 'html.parser')
            fetch_data(soup)

    except Exception as e:
        print(f"An error occurred: {e}")

def save_to_csv(data,rank_dict):
    with open("Euro_2024_Matches.csv",'w',newline='') as file:
        wr = csv.writer(file)
        wr.writerow(["stadium","attendance","home_team",'away_team','home_goals','away_goals',
    'Expected goals (xG)','Total shots','Shots on target','Big chances',
    'Big chances missed','Accurate passes','Fouls committed','Corners',
    'Total shots','Shots off target','Shots on target','Blocked shots',
    'Hit woodwork','Shots inside box','Shots outside box','Expected goals (xG)',
    'xG open play','xG set play','Non-penalty xG','xG on target (xGOT)',
    'Passes','Accurate passes','Own half','Opposition half',
    'Accurate long balls','Accurate crosses','Throws','Touches in opposition box',
    'Offsides','Tackles won','Interceptions','Blocks',
    'Clearances','Keeper saves','Yellow cards','Red cards',
    'Duels won','Ground duels won','Aerial duels won','Successful dribbles'])
        for i in range(len(data['stadium'])):
            row = [
                data['stadium'][i], data['attendance'][i], data['home_team'][i], data['away_team'][i],
                data['home_goals'][i], data['away_goals'][i],
                rank_dict['Expected goals (xG)'][i], rank_dict['Total shots'][i], rank_dict['Shots on target'][i],
                rank_dict['Big chances'][i],
                rank_dict['Big chances missed'][i], rank_dict['Accurate passes'][i], rank_dict['Fouls committed'][i],
                rank_dict['Corners'][i],
                rank_dict['Total shots'][i], rank_dict['Shots off target'][i], rank_dict['Shots on target'][i],
                rank_dict['Blocked shots'][i],
                rank_dict['Hit woodwork'][i], rank_dict['Shots inside box'][i], rank_dict['Shots outside box'][i],
                rank_dict['Expected goals (xG)'][i],
                rank_dict['xG open play'][i], rank_dict['xG set play'][i], rank_dict['Non-penalty xG'][i],
                rank_dict['xG on target (xGOT)'][i],
                rank_dict['Passes'][i], rank_dict['Accurate passes'][i], rank_dict['Own half'][i],
                rank_dict['Opposition half'][i],
                rank_dict['Accurate long balls'][i], rank_dict['Accurate crosses'][i], rank_dict['Throws'][i],
                rank_dict['Touches in opposition box'][i],
                rank_dict['Offsides'][i], rank_dict['Tackles won'][i], rank_dict['Interceptions'][i],
                rank_dict['Blocks'][i],
                rank_dict['Clearances'][i], rank_dict['Keeper saves'][i], rank_dict['Yellow cards'][i],
                rank_dict['Red cards'][i],
                rank_dict['Duels won'][i], rank_dict['Ground duels won'][i], rank_dict['Aerial duels won'][i],
                rank_dict['Successful dribbles'][i]
            ]
            wr.writerow(row)
def main():
    original_link = "https://www.fotmob.com/leagues/50/matches/euro/by-round"
    driver = Functions.setup_driver()
    driver.get(original_link)
    try:
        # Round 1
        which_round = Select(driver.find_element(By.CLASS_NAME, "css-gk6f5k-Select"))
        which_round.select_by_visible_text("Round 1")
        fetch_matches(driver)
        #Round 2
        driver = Functions.setup_driver()
        driver.get(original_link)
        which_round = Select(driver.find_element(By.CLASS_NAME, "css-gk6f5k-Select"))
        which_round.select_by_visible_text("Round 2")
        fetch_matches(driver)
        print(rank_dict['Expected goals (xG)'])
        print(data['home_team'])
        save_to_csv(data,rank_dict)
    except Exception as e:
        print(f"an error occurred {e}")
    finally:
        driver.quit()


if __name__ == "__main__":
    main()
