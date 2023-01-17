import requests
import bs4
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
import numpy as np

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


def onclick(event):
    ax = plt.gca()
    # ax.set_title(f"You selected {event.x}, {event.y}")

    line = event.artist
    #xdata, ydata = line.get_data()
    ind = event.ind
    x = gdf.iloc[event.ind[0]]['longitude']
    y = gdf.iloc[event.ind[0]]['latitude']
    parkrun_name = gdf.iloc[event.ind[0]]['parkrun_name']
    tx = f"x={x}, y={y}, parkrun={parkrun_name}"

    ax.set_title(f"{tx}")

# Get distinct list of parkruns attended
# Join to parkrun master list to obtain lat and long
# Plot on Map display :D

if __name__ == '__main__':

    df = get_parkrun_info(PARKRUN_ID)
    events = get_parkrun_events_list()
    df = pd.merge(events, df, how='left', left_on='parkrun_name', right_on='Event').drop(columns=['Event'])

    uk = gpd.read_file('uk.geojson')

    gdf = gpd.GeoDataFrame(
        df, geometry=gpd.points_from_xy(df.longitude, df.latitude)
    )
    gdf.crs = "EPSG:4326"
    gdf = gdf.to_crs(uk.crs)

    fig = plt.figure(figsize=(10, 10))
    ax = fig.add_subplot(111)
    uk.plot(ax=ax, alpha=0.8)

    # gdf.plot(ax=ax, color='yellow', marker='.', markersize=8, alpha=0.2, picker=20)
    gdf[gdf['Run Date'].isna()].plot(ax=ax, color='black', marker='.', markersize=8, alpha=0.2, picker=50)
    gdf[gdf['Run Date'].notna()].plot(ax=ax, color='#AAFF00', marker='.', markersize=50, picker=50)

    ax.set_xlim(-7, 2)
    ax.set_ylim(49, 60)

    cid = fig.canvas.mpl_connect('pick_event', onclick)

    plt.show()