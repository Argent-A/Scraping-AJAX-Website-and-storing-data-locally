#   ---------------------------------------------------------------------------   #
#   --------------------    Import Modules                ---------------------   #
#   ---------------------------------------------------------------------------   #

import sqlite3
import os
import sys
from bs4 import BeautifulSoup
import re
from datetime import datetime
from selenium import webdriver
import time
import random
from urllib.request import Request, urlopen



#   ---------------------------------------------------------------------------   #
#   --------------------    Establish Chrome Path & url   ---------------------   #
#   ---------------------------------------------------------------------------   #
chrome_path = r'C:\Users\Argen\Desktop\Python Scripts\Drivers\chromedriver.exe'
driver = webdriver.Chrome(chrome_path)
url = "REDACTED"

def reset_url():
    driver.get(url)

#   ---------------------------------------------------------------------------   #
#   --------------------    Establish Database  Connection     ----------------   #
#   ---------------------------------------------------------------------------   #


os.chdir(r'C:\Users\Argen\Desktop\Python Scripts\Databases')
DB_Connection = sqlite3.connect("Welcome Home.sqlite")
cursor = DB_Connection.cursor()
cursor.execute('''CREATE TABLE IF NOT EXISTS SUNNYSIDE_PROPERTIES (
TITLE TEXT,
LISTING_TYPE TEXT,
AREA TEXT,
ADDRESS TEXT,
URL_LINK TEXT PRIMARY KEY UNIQUE,
DB_ENTRY_DATE TEXT,
DB_ENTRY_TIME TEXT
)''')

#   -----------------------------------------------------------------------------------------------------   #
#   --------------------    Scrape Through Results & Enter Links into Database           ----------------   #
#   -----------------------------------------------------------------------------------------------------   #

#traverse through webpage's xpaths
def xpath_iterator(org_path_value, random_path_value):
    time.sleep(1)
    # jump from 1st to 2nd page
    if org_path_value == 1:
        initial_xpath = '''/html/body/div['''+str(random_path_value)+''']/div[6]/div/div/div/div[1]/ul/li[1]/a'''
        path_value = org_path_value + 1
        next_xpath = ('''/html/body/div['''+str(random_path_value)+''']/div[6]/div/div/div/div[1]/ul/li[''' +str(path_value)+''']/a''')
        print('page', org_path_value, 'to', path_value)

    # jump from 2nd to 3rd page , 3rd to 4th page
    elif (org_path_value > 1) and (org_path_value < 4) :
        initial_xpath = '''/html/body/div['''+str(random_path_value)+''']/div[6]/div/div/div/div[1]/ul/li['''+str(org_path_value+1)+ ''']/a'''
        path_value = org_path_value + 2
        next_xpath = ('''/html/body/div['''+str(random_path_value)+''']/div[6]/div/div/div/div[1]/ul/li[''' + str(path_value) + ''']/a''')
        print('page', org_path_value, 'to', path_value - 1)
        next_xpath
    else:
        initial_xpath = '''/html/body/div['''+str(random_path_value)+''']/div[6]/div/div/div/div[1]/ul/li[''' + str(org_path_value + 1) + ''']/a'''
        next_xpath = ('''/html/body/div['''+str(random_path_value)+''']/div[6]/div/div/div/div[1]/ul/li[''' + str(5) + ''']/a''')
        path_value = org_path_value + 1
        print('page', org_path_value, 'to', path_value)
    print('moving from', initial_xpath, 'to', next_xpath)
    return next_xpath

reset_url()


#A walkthrough of one session's xpath
#page 1 -> 2
    # /html/body/div[3]/div[6]/div/div/div/div[1]/ul/li[2]/a [correct]
#page 2 -> 3
    # /html/body/div[2]/div[6]/div/div/div/div[1]/ul/li[4]/a [correct]
#page 3 - > 4
    # /html/body/div[2]/div[6]/div/div/div/div[1]/ul/li[5]/a [correct]
#page 4 -> 5
    # /html/body/div[2]/div[6]/div/div/div/div[1]/ul/li[5]/a [correct]
#page 5 -> 6
    # /html/body/div[2]/div[6]/div/div/div/div[1]/ul/li[5]/a [correct]
#page 6 -> 7
    # /html/body/div[2]/div[6]/div/div/div/div[1]/ul/li[5]/a [correct]
#page 7 -> 8
    # /html/body/div[2]/div[6]/div/div/div/div[1]/ul/li[5]/a [correct]
    # etc . . .

#Takeways:
    # the first index is subject to change, either a [2] or a [3]
    # the second index is always constant [6]
    # the third index is [2] on first page, [4] on second page, and [5] on every other consecutive page
        # jumping from first to second page, the path value index goes up by 1 [1] - > [2]
        # jumping from second to third page, the path value index goes up by 2 [2] -> [4]
        # jumping after, the path value is always [5].





#Click agree button on front page of site
try:
    time.sleep(random.uniform(0.1, 0.2))
    driver.find_element_by_xpath(r'//*[@id="compliance-footer"]/div/div[2]/button').click()
    print('AGREE CLICKED')
except:
    print('AGREE NOT FOUND')


path_value = 0
old_urls = set()
new_urls = set()

while True:
# FIRST PAGE ##############################################################################
    if path_value == 0:
        first_html = driver.page_source #extract all page html
        bs = BeautifulSoup(first_html, 'html.parser')
        tag = bs('a') # grab all html with the A tag
        for each in tag:
            LINK = each.get('href') # grab link from line
            TITLE = each.get('title') # grab title from line
            TITLE = str(TITLE)
            LINK = str(LINK)
            if TITLE is None: continue
            if TITLE == 'None': continue
            if ("welcomehome" in LINK) == False: continue
            print("___________________")
            print("LINK:", LINK, "\n", "TITLE:", TITLE)
            path_value = 1 # establish that we are no longer on the first page
            # push links into database
            cursor.execute('SELECT URL_LINK FROM SUNNYSIDE_PROPERTIES WHERE URL_LINK = ? LIMIT 1', (LINK,))
            try:
                cursor.fetchone()[0]
                print("url is already stored in database, proceeding with next url")
                time.sleep(0.05 + random.uniform(0.001, 0.01))
                old_urls.add(TITLE + " " + LINK)
            except:
                print('adding new url to database')
                new_urls.add(TITLE + " " + LINK)
                time.sleep(0.05 + random.uniform(0.001, 0.02))
                AREA = LINK.split(sep="/")[3]
                LISTING_TYPE = LINK.split(sep="/")[4]
                ADDRESS = LINK.split(sep="/")[5]
                DATE = str(datetime.now()).split()[0]
                TIME = (str(datetime.now()).split()[1])[0:5]
                cursor.execute(
                    '''INSERT OR IGNORE INTO SUNNYSIDE_PROPERTIES (TITLE, LISTING_TYPE, AREA, ADDRESS,  URL_LINK, DB_ENTRY_DATE, DB_ENTRY_TIME) VALUES(?,?,?,?,?,?,?)''',
                    (TITLE, LISTING_TYPE, AREA, ADDRESS, LINK, DATE, TIME))

        DB_Connection.commit()

# THEREAFTER ##############################################################################



    else:
        try:
            time.sleep(random.uniform(0.01, 0.03))
            next_xpath = xpath_iterator(path_value, 2) # since the first index value alternates we try both 2 & 3
            print('searching', url, 'and xpath value:', next_xpath)
            driver.find_element_by_xpath(next_xpath).click()
            print('path found extracting HTML')

        except:
            try:
                time.sleep(random.uniform(0.01, 0.03))
                next_xpath = xpath_iterator(path_value, 3) # since the first index value alternates we try both 2 & 3
                print('searching', url, 'and xpath value:', next_xpath)
                driver.find_element_by_xpath(next_xpath).click()
                print('path found extracting HTML')
            except:
                print('neither random path found or traversed all pages')
                break # break condition of while loop
        path_value += 1

        html = driver.page_source
        bs = BeautifulSoup(html, 'html.parser')
        tag = bs('a')
        for each in tag:
            LINK = each.get('href')
            TITLE = each.get('title')
            TITLE = str(TITLE)
            LINK = str(LINK)
            if TITLE is None : continue
            if TITLE == 'None': continue
            if ("welcomehome" in LINK) == False: continue
            print("___________________")
            print("LINK:", LINK, "\n", "TITLE:", TITLE)
            cursor.execute('SELECT URL_LINK FROM SUNNYSIDE_PROPERTIES WHERE URL_LINK = ? LIMIT 1', (LINK,))
            try:
                cursor.fetchone()[0]
                print("url is already stored in database, proceeding with next url")
                old_urls.add(TITLE + " " +LINK)
            except:
                print('adding new url to database')
                new_urls.add(TITLE + " " + LINK)
                AREA = LINK.split(sep="/")[3]
                LISTING_TYPE = LINK.split(sep="/")[4]
                ADDRESS = LINK.split(sep="/")[5]
                DATE = str(datetime.now()).split()[0]
                TIME = (str(datetime.now()).split()[1])[0:5]
                cursor.execute(
                    '''INSERT OR IGNORE INTO SUNNYSIDE_PROPERTIES (TITLE, LISTING_TYPE, AREA, ADDRESS,  URL_LINK, DB_ENTRY_DATE, DB_ENTRY_TIME) VALUES(?,?,?,?,?,?,?)''',
                    (TITLE, LISTING_TYPE, AREA, ADDRESS, LINK, DATE, TIME))
        DB_Connection.commit()


count_new_record = 0
for each in new_urls:
    count_new_record += 1

count_old_record = 0
for each in old_urls:
    count_old_record += 1

print(count_new_record, "New Entries inserted into SUNNYSIDE_PROPERTIES")
for each in new_urls:
    print(each)
print(count_old_record, "Records already in SUNNYSIDE_PROPERTIES")

DB_Connection.commit()


# Additional table alters done retro-actively
# cursor.execute('''ALTER TABLE SUNNYSIDE_PROPERTIES ADD COLUMN SIZE TEXT''')
# cursor.execute(('''ALTER TABLE SUNNYSIDE_PROPERTIES ADD COLUMN CONTRACT_STATUS TEXT'''))
# cursor.execute(('''ALTER TABLE SUNNYSIDE_PROPERTIES ADD COLUMN PROPERTY_PRICE TEXT'''))
# cursor.execute(('''ALTER TABLE SUNNYSIDE_PROPERTIES ADD COLUMN AMENITIES TEXT'''))
# cursor.execute(('''ALTER TABLE SUNNYSIDE_PROPERTIES ADD ADDITIONAL_INFO TEXT'''))
# cursor.execute(('''ALTER TABLE SUNNYSIDE_PROPERTIES ADD URL_STATUS TEXT'''))
# cursor.execute(('''ALTER TABLE SUNNYSIDE_PROPERTIES ADD LATEST_ENTRY_TIME TEXT'''))
# cursor.execute(('''ALTER TABLE SUNNYSIDE_PROPERTIES ADD LATEST_ENTRY_DATE TEXT'''))


# ###############################################################################
# ##################            Grab URL Data            #######################
# ###############################################################################

# ##                       randomize user agents:                        ####
user_agent_list = [
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.1.1 Safari/605.1.15',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:77.0) Gecko/20100101 Firefox/77.0',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:77.0) Gecko/20100101 Firefox/77.0',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36',
]

randomize_user = random.uniform(0, 4)
user = user_agent_list[int(randomize_user)]
headers = {'User-Agent': user}

stored_urls = cursor.execute('''SELECT URL_LINK, LATEST_ENTRY_DATE, CONTRACT_STATUS FROM SUNNYSIDE_PROPERTIES''')
url_list = list()
count_total_urls = 0


# ##                    Define which URLs are in scope:                        ####

for record in stored_urls:
    link = record[0]
    latest_date_entry = str(record[1])
    contract_status = str(record[2])
    try:
        Today = datetime.strptime(str(datetime.now()).split()[0], '%Y-%m-%d').date()
        Record_Date = datetime.strptime(str(latest_date_entry).split()[0], '%Y-%m-%d').date()
        Date_Distance = abs((Today - Record_Date).days)
        print(Date_Distance)
    except:
        Today = "TRUE"
        print('Record was received today')
        Date_Distance = 0

    if contract_status == "LISTING GONE":
        continue
    if Today == "TRUE" or Date_Distance == 0:
        url_list.append(link)
        count_total_urls += 1
    if Date_Distance > 3:
        url_list.append(link)
        count_total_urls += 1

print("Total URLs in Scope:" + str(count_total_urls))

#   ---------------------------------------------------------------------------   #
#   --------------------    Scrape Supplemental Data:     ---------------------   #
#   ---------------------------------------------------------------------------   #

for url in url_list:
    print(url)

failed_urls = list()
lookups = 0
cnt_failed = 0
for target_url in url_list:
    time.sleep(random.uniform(1, 8))
    req = Request(target_url, headers = headers)
    webpage = urlopen(req, timeout = 30).read()
    bspage = BeautifulSoup(webpage, 'html.parser')

    try:
        url_check = str(bspage.find('h1', attrs={'class': "text-center"}).text).strip()
        type(url_check)
        if url_check == 'Sorry, the property you are looking for does not exist.':
            print('URL No Longer Available')
            cnt_failed += 1
            URL_STATUS = 'URL NO LONGER AVAILABLE'
            Contract_Status = 'LISTING GONE'
            cursor.execute('''UPDATE SUNNYSIDE_PROPERTIES SET URL_STATUS = ? WHERE URL_LINK = ?''',
                               (URL_STATUS, target_url))
            cursor.execute('''UPDATE SUNNYSIDE_PROPERTIES SET CONTRACT_STATUS = ? WHERE URL_LINK = ?''',
                               (Contract_Status, target_url))
            continue
    except:
        URL_STATUS = "URL AVAILABLE SINCE LAST ENTRY DATE"

    print(URL_STATUS)

    #Latest entry time
    LATEST_TIME = (str(datetime.now()).split()[1])[0:5]
    #Latest entry date
    LATEST_DATE = str(datetime.now()).split()[0]
    #Contract Status
    lookups += 1
    try:
        Contract_Status = bspage.find('div', attrs={'class': "label in-contract"}).text
        Contract_Status = str(Contract_Status).strip()
    except:
        Contract_Status = str('Available')
    #Property Price
    try:
        Property_Price = bspage.find('h2', attrs={'class': "property-price-header"}).text
        Property_Price = str(Property_Price).strip()
    except:
        Property_Price = 'Price Not Mentioned'
    # additional information
    try:
        additional_info = (bspage.findAll('div', attrs={
            "style": "font-size: 16px;line-height:2;font-weight: bold;vertical-align: middle;display: flex;align-items: center;justify-items: center;align-content: center;"}))
        count = 0
        for each in additional_info:
            count += 1
            if count == 1: continue  # this is usually the second div tag
            additional_info = str(each.text).strip()
        if additional_info == []:
            additional_info = str('Additional Info Was Not Available')
    except:
        additional_info = str('Additional Info Was Not Available')
    # Amenities
    try:
        Amenities = ""
        unit_details = (bspage.findAll('li', attrs={"amenity"}))
        track = 0
        for each in unit_details:
            if track == 0:
                Amenities = str(each.text)
                track += 1
            else:
                Amenities = (Amenities + "," + str(each.text))
    except:
        Amenities = str('Amenities Not Listed')
    print(('\r\n\r\n'))
    print("******************************************************************")
    print("=================================================================|")
    print('====              Grabbing Data For Address:                 ==== ')
    print("=================================================================|")
    print(str(target_url).split(sep="/")[5])
    print("=================================================================|")
    print("Property Price: " + str(Property_Price))
    print("_________________________________________________________________|")
    print('Additional Info: ' + str(additional_info))
    print("_________________________________________________________________|")
    print('Amenities: ' + str(Amenities))
    print("_________________________________________________________________|")
    print('Contract Status: ' + str(Contract_Status))
    print("_________________________________________________________________|")
    print("****************************END***********************************")
    cursor.execute('''UPDATE SUNNYSIDE_PROPERTIES SET PROPERTY_PRICE = ? WHERE URL_LINK = ?''', (Property_Price, target_url))
    cursor.execute('''UPDATE SUNNYSIDE_PROPERTIES SET ADDITIONAL_INFO = ? WHERE URL_LINK = ?''', (additional_info, target_url))
    cursor.execute('''UPDATE SUNNYSIDE_PROPERTIES SET AMENITIES = ? WHERE URL_LINK = ?''', (Amenities, target_url))
    cursor.execute('''UPDATE SUNNYSIDE_PROPERTIES SET CONTRACT_STATUS = ? WHERE URL_LINK = ?''', (Contract_Status, target_url))
    cursor.execute('''UPDATE SUNNYSIDE_PROPERTIES SET URL_STATUS = ? WHERE URL_LINK = ?''',(URL_STATUS, target_url))
    cursor.execute('''UPDATE SUNNYSIDE_PROPERTIES SET LATEST_ENTRY_TIME = ? WHERE URL_LINK = ?''',(LATEST_TIME, target_url))
    cursor.execute('''UPDATE SUNNYSIDE_PROPERTIES SET LATEST_ENTRY_DATE = ? WHERE URL_LINK = ?''',(LATEST_DATE, target_url))

DB_Connection.commit()

print('Total URLS provided: ' + str(count_total_urls))
print('Total failed urls: ' + str(cnt_failed))
print(('Total URLS searched: ' + str(lookups)))


# #####################################################################################################
# ##################            Derived Additional Database fields            #########################
# #####################################################################################################

apts_info = list()
for each in cursor.execute('''SELECT*FROM SUNNYSIDE_PROPERTIES'''):
    description = each[0]
    if (str(description).split()[0]).upper() == "STUDIO":
        size = 'STUDIO'
    else:
        size = (str(description).split()[0]).upper() + " " + (str(description).split()[1]).upper()
    url = (each[4])
    apt_data = (size, url)
    apts_info.append(apt_data)

for record in apts_info:
    print(record)
    cursor.execute('''UPDATE SUNNYSIDE_PROPERTIES SET SIZE = ? WHERE URL_LINK = ?''', (record[0], record[1]))
DB_Connection.commit()


DB_Connection.close()



# ###############################################################################################################
# ##################                         Draft Email using GMAIL                    #########################
# ###############################################################################################################
sys.path.append(r'C:\Users\Argen\Desktop\Python Scripts\Scripts\(Index 1) Python For Everybody Scripts')

import PyMail
#List of Emails


emails = open("Emails.txt").read()
emails = (emails.split('\n'))

for value in emails:
    if len(value) == 0:
        emails.remove(value)

url_message = str()

for entry in new_urls:
    url_message = str(url_message) + '\r\n' + entry

print(url_message)


#Email Subject
todays_date = str(datetime.now()).split()[0]
title = str("Latest Listings For ") + str(todays_date)


#Email Message
Message = str("These are the latest listings from REDACTED") + "\r\n" + str(url_message)
print(Message)
remove = "<>"


#def send_email(TO_ADDRESS, subject, message):
list_of_emails = set()
for each in emails:
    user_name = each.split(" ")[0]
    user_email = re.sub(remove, "",  (each.split(" ")[2]))
    user_email = ((each.split(" ")[2]).split("<")[1]).split('>')[0]
    msg = str(user_name + ",\r\n") + Message
    print("sending:\r\n", str(title), "\r\n", str(msg))
    PyMail.send_email(user_email, title, msg)













