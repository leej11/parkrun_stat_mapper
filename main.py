import requests
import bs4
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
import pandas as pd

# Inspired by code from this: https://github.com/caffreit/Park-Run-Scraper



PARKRUN_ID = 6486341

def get_parkrun_info(parkrunner_id):

    service = Service("~/PycharmProjects/drivers/chromedriver_mac64/chromedriver")
    op = webdriver.ChromeOptions()
    driver = webdriver.Chrome(service=service, options=op)
    URL = f"https://www.parkrun.org.uk/parkrunner/{parkrunner_id}/all/"
    driver.get(URL)
    src = driver.page_source
    soup = bs4.BeautifulSoup(src, "html.parser")
    table = soup.find_all("table")
    df = pd.read_html(str(table))[2] # There's 3 tables, the 3rd (index=2) is the one with all runs

    driver.close()

    return df

def get_parkrun_events_list():
    # This website shared a list of parkruns and their lat/longs
    # https://www.moreofless.co.uk/alphabetical-list-uk-parkrun-events-spreadsheet
    events = pd.read_csv('uk-parkruns.csv', header=None, names=['parkrun_name', 'location_name', 'longitude', 'latitude'])
    return events


# Get distinct list of parkruns attended
# Join to parkrun master list to obtain lat and long
# Plot on Map display :D

if __name__ == '__main__':

    df = get_parkrun_info(PARKRUN_ID)
    
    print(df)

    print("=" * 80)

    events = get_parkrun_events_list()
    print(events.head(100))