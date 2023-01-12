import requests
import bs4
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
import pandas as pd

service = Service("~/PycharmProjects/drivers/chromedriver_mac64/chromedriver")
op = webdriver.ChromeOptions()
driver = webdriver.Chrome(service=service, options=op)

PARKRUN_ID = 6486341

def get_parkrun_info(parkrunner_id):

    URL = f"https://www.parkrun.org.uk/parkrunner/{parkrunner_id}/all/"
    driver.get(URL)
    print(driver.title)
    src = driver.page_source
    soup = bs4.BeautifulSoup(src, "html.parser")
    table = soup.find_all("table")

    driver.close()

    return table

def get_parkrun_events_list():
    # This website shared a list of parkruns and their lat/longs
    # https://www.moreofless.co.uk/alphabetical-list-uk-parkrun-events-spreadsheet
    events = pd.read_csv('uk-parkruns.csv', header=None, names=['parkrun_name', 'location_name', 'longitude', 'latitude'])
    return events




if __name__ == '__main__':

    table = get_parkrun_info(PARKRUN_ID)
    tmp_df = pd.read_html(str(table))[2]
    print(tmp_df)

    print("=" * 80)

    events = get_parkrun_events_list()
    print(events.head(100))