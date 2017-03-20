# -*- coding: utf-8 -*-
"""
Created on Mon Mar 20 09:10:16 2017

@author: araveret
"""

# Content from Alex Sherman

'''
PART ONE
    learn how to read html with requests &
    scrape data with Beautiful Soup 
'''

# requests
import requests

url = r'https://raw.githubusercontent.com/Alexjmsherman/python_for_data_analysis/master/Data_Scraping_APIs_and_Automation/data/example_html.html'
r = requests.get(url)
r.status_code
r.text

# read html into Beautiful Soup
from bs4 import BeautifulSoup

b = BeautifulSoup(r.text)


# .find
b.find('title')

# .text
b.find('title').text

# .attrs
b.find('p', attrs={'id':'scraping'}).text

# select attribute
b.find('h1')['id']

# .find_all
b.find_all('p')

# slice the results
paragraphs = b.find_all('p')
paragraphs[0]  # view the first item (index starts at 0)
paragraphs[1]  # view the second item
paragraphs[1:3] # view 1 & 2 (inclusive first #; exclusive last #)
paragraphs[-1]  # view the last item

# iterate over the results
for p in paragraphs:
    print(p.text)

'''
EXERCISE ONE
'''

# find the 'h2' tag and then print its text
b.find('h2').text

# find the 'p' tag with an 'id' value of 'reproducibility' 
# and then print its text
b.find('p', attrs={'id':'reproducibility'}).text

# find the first 'p' tag and then print the value of the 'id' attribute
b.find('p')['id']

# print the text of all four li tags
li = b.find_all('li')
for l in li:
    print(l.text)

# bonus question: print the text of only the API resources
li = b.find('ul', attrs={'id':'api'}).find_all('li')
for l in li:
    print(l.text)


'''
PART TWO
    analyze HTML from opm.gov
'''

# HTML from opm.gov
url = r'https://www.opm.gov/'
r = requests.get(url)
b = BeautifulSoup(r.text)

# find the first blog post
blog = b.find_all('div', attrs={'class':'Blog_Entry'})[0]

# get the blog Title
blog.find('div', attrs={'class':'Blog_Title'}).text

# get the date the blog was posted
blog.find('div', attrs={'class':'Blog_Date'}).text

# get the blog text
blog.find('p', attrs={'class':'Blog_Text'}).text


'''
EXERCISE 2
'''

# HTML from opm.gov/data
url = r'https://www.opm.gov/data/Index.aspx?tag=FedScope'
r = requests.get(url)
b = BeautifulSoup(r.text)

# find the html for the table of files (HINT: look for the class DataTable)
data_table = b.find('table', attrs={'class':'DataTable'})

# find the html for the first row of files (HINT: make sure to skip the table headers)
data_table.find_all('tr')[1]

# find the 'td' element with the .zip link (HINT: look for 'a href')
url = data_table.find_all('td')[2]

# get the zip url
url.find('a')['href']


'''
PART THREE
    -Use selenium for web browser automation
'''

from selenium import webdriver
from selenium.webdriver.common.keys import Keys

# specify which browser to use (Chrome)
# https://chromedriver.storage.googleapis.com/index.html?path=2.25/
browser = webdriver.Chrome(r'chromedriver\chromedriver.exe')
browser.implicitly_wait(2)

# open a browser
browser.get(r'https://www.opm.gov/data/Index.aspx?tag=FedScope')

# select an item in the sort by box
browser.find_element_by_xpath(
    r'//*[@id="ctl01_ctl00_MainContentPlaceHolder_MainContentPlaceHolder_SortCol"]/option[2]').click()

### Press 'go' button
browser.find_element_by_xpath(
    r'//*[@id="ctl01_ctl00_MainContentPlaceHolder_MainContentPlaceHolder_Filter"]').click()

# type and submit a query in the search box
inputbox = browser.find_element_by_xpath(
    r'//*[@id="ctl01_ctl00_MainContentPlaceHolder_MainContentPlaceHolder_SearchTerm"]')
inputbox.send_keys('OPM')
inputbox.send_keys(Keys.ENTER)

# select the assessment drop down
browser.find_element_by_xpath(r'//*[@id="SecondaryNavigation"]/li[1]/a[2]').click()

# get_first_zip_link
html = browser.find_element_by_xpath(
    r'//*[@id="ctl01_ctl00_MainContentDiv"]/table/tbody/tr[2]/td[3]/span/a')
link = html.get_attribute('href')

# close the browser
browser.close()

# download and open the zip file
from download_zip import download_zip_file
data = download_zip_file(link, pandas=True)
data.open_zip()


'''
PART FOUR
    -APIs
'''

# XML
xml_url = r'https://raw.githubusercontent.com/Alexjmsherman/python_for_data_analysis/master/Data_Scraping_APIs_and_Automation/data/example_xml.xml'
r = requests.get(xml_url)
b = BeautifulSoup(r.text, 'xml')

# find the fourth topic
b.find_all('NAME')[3]

# collect data from google maps api
# documentation: https://developers.google.com/maps/documentation/geocoding/start
address = 'TYPE AN ADDRESS HERE'
api_url = r'https://maps.googleapis.com/maps/api/geocode/xml?address={}'.format(address)
r = requests.get(api_url)
b = BeautifulSoup(r.text, 'xml')

# find the status code
b.find('status').text

# find the postal code
address_components = b.find_all('address_component')
for address in address_components:
    address_type = address.find('type').text
    if 'postal_code' in address_type:
        print(address.find('long_name').text)

# find the latitude and longitude
latitude = b.find('location').find('lat').text
longitude = b.find('location').find('lng').text

# use a python api wrapper package for google maps
# https://github.com/googlemaps/google-maps-services-python
import googlemaps  

gmaps = googlemaps.Client(key='INSERT YOUR API KEY HERE')
gmaps.reverse_geocode((latitude,longitude))
gmaps.places('Cosi', location=(latitude, longitude), radius=1000)

# json
import json

# The missing JSON inspector for chrome 
# https://chrome.google.com/webstore/detail/the-missing-json-inspecto/hhffklcokfpbcajebmnpijpkaeadlgfn
address = 'TYPE AN ADDRESS HERE'
api_json_url = r'https://maps.googleapis.com/maps/api/geocode/json?address={}'.format(address)
r = requests.get(api_json_url)

# get the latitude and longitude from json
j = json.loads(r.text)
j['results'][0]['geometry']['location']['lat']
j['results'][0]['geometry']['location']['lng']