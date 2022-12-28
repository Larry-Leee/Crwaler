# import libraries
from bs4 import BeautifulSoup
import requests
import csv
import datetime
import pandas as pd
import smtplib
import time


# connect to the website i would like to do a web scraping; httpbin.org/get
URL = 'https://www.amazon.co.uk/s?k=skII&crid=2CAHDTR5AV0UH&sprefix=skii%2Caps%2C408&ref=nb_sb_noss_1'
headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.61 Safari/537.36",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    "Upgrade-Insecure-Requests": "1", "Connection": "close", "DNT": "1"}
page = requests.get(URL, headers=headers)

soup = BeautifulSoup(page.content, "html.parser")
# formatted
lists = BeautifulSoup(soup.prettify(), "html.parser")
date = datetime.date.today()
# test
# print(lists)
allResults = lists.find_all('div', {'data-component-type': 's-search-result'})
item1 = allResults[0]
#get item


#getting the next page
def get_url(search_term):
    """Getting the url rom search term"""
    template = 'https://www.amazon.co.uk/s?k={}&crid=3N0ELJIE9O4L0&sprefix=%2Caps%2C98&ref=nb_sb_ss_recent_1_0_recent'
    #replace space with +
    search_term = search_term.replace(' ', '+')
    #add term query to url
    url = template.format(search_term)
    #add page query placeholder
    url += '&page{}'
    return url


url = get_url('basketball')


# generalise the pattern
def extract_record(item):
    """Extract and return data from a single record"""
    atag = item.h2.a
    description = atag.text.strip()
    # print(description)
    #url
    url = 'https://www.amazon.com' + atag.get('href')
    #get price
    try:
        prcie_parent = item.find('span', {'class': 'a-price'})
        price = prcie_parent.find('span', {'class': 'a-offscreen'}).get_text()
    except AttributeError:
        return
    #get review
    try:
        rating_parent = item.find('i', {'class': 'a-icon'})
        rating = rating_parent.find('span', {'class': 'a-icon-alt'}).get_text()
    except AttributeError:
        rating = ''

    #review_count
    try:
        review_count = item.find('span', {'class': 'a-size-base'}).get_text()
        # print(review_count)
    except AttributeError:
        review_count = ''
    result = (description, price, rating, review_count, url, date)
    return result


records = []


for page in range(1, 21):
    lists = BeautifulSoup(soup.prettify(), "html.parser")
    results = lists.find_all('div', {'data-component-type': 's-search-result'})

    for item in results:
        record = extract_record(item)
        if record:
            records.append(record)


    #save the data into csv
    with open('AmazonWebScraperDataset.csv', 'w', encoding='utf-8', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['Description', 'Price', 'Rating', 'Review Count', 'URL', 'Date'])
        writer.writerows(records)
        df = pd.read_csv('/Users/lihang/PycharmProjects/crwal/AmazonWebScraperDataset.csv')
        print(df)
















