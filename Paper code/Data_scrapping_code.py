import random
import pandas as pd
import requests
from bs4 import BeautifulSoup
from random import randint
from time import sleep
import random

proxies = []
AGENT_LIST = [{'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:77.0) Gecko/20100101 Firefox/77.0',
               'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
               'Accept-Language': 'en-US,en;q=0.5',
               'Referer': 'https://www.google.com/', 'DNT': '1', 'Connection': 'keep-alive',
               'Upgrade-Insecure-Requests': '1'},
              {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:77.0) Gecko/20100101 Firefox/77.0',
               'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
               'Accept-Language': 'en-US,en;q=0.5', 'Accept-Encoding': 'gzip, deflate, br',
               'Referer': 'https://www.google.com/',
               'DNT': '1', 'Connection': 'keep-alive', 'Upgrade-Insecure-Requests': '1'},
              {'Connection': 'keep-alive', 'DNT': '1',
               'Upgrade-Insecure-Requests': '1',
               'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36',
               'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
               'Sec-Fetch-Site': 'none',
               'Sec-Fetch-Mode': 'navigate',
               'Sec-Fetch-Dest': 'document',
               'Referer': 'https://www.google.com/',
               'Accept-Encoding': 'gzip, deflate, br',
               'Accept-Language': 'en-GB,en-US;q=0.9,en;q=0.8'},
              {'Connection': 'keep-alive',
               'Upgrade-Insecure-Requests': '1',
               'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36',
               'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
               'Sec-Fetch-Site': 'same-origin',
               'Sec-Fetch-Mode': 'navigate',
               'Sec-Fetch-User': '?1',
               'Sec-Fetch-Dest': 'document',
               'Referer': 'https://www.google.com/',
               'Accept-Encoding': 'gzip, deflate, br',
               'Accept-Language': 'en-US,en;q=0.9'}]
header = random.choice(AGENT_LIST)
page_url = []
review_all = []
page_num = 0

#Only update this url with another companies glass door link
url = 'https://www.glassdoor.com/Reviews/Ahsanullah-University-of-Science-and-Technology-Reviews-E386407.htm?sort.sortType=OR&sort.ascending=true&filter.iso3Language=eng'

def getdata(url):
    response = requests.request('get', url,headers=header)
    print(response.status_code)
    soup = BeautifulSoup(response.content, features="lxml")
    return soup


#Edit Company Name
def get_reviews(soup):
    reviews = soup.findAll('li', class_='noBorder empReview cf pb-0 mb-0')
    for review in reviews:
        ratings = review.find('div', class_='d-flex align-items-center mb-0 mb-md-sm css-1x8nk7l eg4psks1').span.text
        job_status = review.find('span', class_='pt-xsm pt-md-0 css-1qxtz39 eg4psks0').text
        pros = review.findAll('span', {'data-test': 'pros'})
        cons = review.findAll('span', {'data-test': 'cons'})
        review_info = {
          'Company Name': 'AUST',
          'Rating': ratings,
          'Job Status': job_status,
          'Pros': pros[0].text,
          'Cons': cons[0].text
        }
        review_all.append(review_info)


def get_pagelink(url):
    page_url.append(url)
#Update Range
    for i in range(2, 5):
        #url = "https://www.glassdoor.com/Reviews/Amazon-Reviews-E6036_P" + str(i) + ".htm?filter.iso3Language=eng"
        url = "https://www.glassdoor.com/Reviews/Ahsanullah-University-of-Science-and-Technology-Reviews-E386407_P" + str(i) + ".htm?sort.sortType=OR&sort.ascending=true&filter.iso3Language=eng"
        page_url.append(url)


get_pagelink(url)
try:
    for link in page_url:
        soup = getdata(link)
        sleep(randint(10, 40))
        get_reviews(soup)
        print("Current page num" + str(page_num))
        page_num = page_num + 1
except:
    pass


df = pd.DataFrame(review_all)
df.to_excel('AUST.xlsx', index=False)
print(page_url)