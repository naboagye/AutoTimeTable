from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import requests
from bs4 import BeautifulSoup
import pandas as pd
import time as t
from utils import * 
import keyring

# Get Credentials from macOS Keychain
usr = keyring.get_password("AutoTimeTable", "username")
pwd = keyring.get_password("AutoTimeTable", str(usr))

# Create a new Google Chrome browser object
chromedriver = '/usr/local/bin/chromedriver'
driver = webdriver.Chrome(chromedriver)

try:
    # Go to login portal and login and submit
    driver.get ("http://ow.ly/Q7uX50BE9h3")
    driver.find_element_by_id("username").send_keys(usr)
    driver.find_element_by_id ("password").send_keys(pwd)
    driver.find_element_by_id("submit").click()    

    # Scrape timetable and save as html file
    t.sleep(5)
    driver.refresh()
    url = driver.current_url
    driver.get(url)
    save_html(driver.page_source, 'timetable2')   

    # Parse and extracts information from time table
    page = open_html('timetable2')
    soup = BeautifulSoup(page, 'html.parser')
    table = soup.find("table", attrs={"id": "timetable_details"})
    table_data = table.tbody.find_all("tr", {'class': 'tt_info_row'})  # contains 2 rows
    i = 1
    for idx, row in enumerate(table_data):
        if idx == 0:
            continue
        day = row.find('div', {'class': 'weekday'}).get_text()
        row = row.find_all("td")
        start = 9
        for r in row:
            if "new_row_tt_info_cell" in str(r):
                start_time = int(str(start)[:-2])
                length = 1
                module_name = r.find('span', {'class': 'tt_module_name_row'}).get_text()
                if r.find('span', {'class': 'tt_room_row'}) == None:
                    location = "Online"
                    start += 1
                    if 'colspan="4"' in str(r):
                        start += 1
                        length = 2
                    createEvent(module_name, start_time, day, length, location, i)
                    i +=1
                else:
                    location = r.find_all('span', {'class': 'tt_room_row'})[0].get_text() + " " + r.find_all('span', {'class': 'tt_room_row'})[1].get_text()
                    start += 1
                    if 'colspan="4"' in str(r):
                        start += 1
                        length = 2
                    createEvent(module_name, start_time, day, length, location, i)
                    i +=1
            elif "new_row_odd_empty_col" in str(r) or "new_row_even_empty_col" in str(r):
                start += .5    
            else:
                continue
        if idx == 5:
            break
except Exception as e:
    print(e)
finally:
    driver.quit()
    

