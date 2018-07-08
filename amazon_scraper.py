from lxml import html
import csv, os, json
import requests
# from exceptions import ValueError
from time import sleep

def AmzonParse(url):
    headers =  {'User-Agent':'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:61.0) Gecko/20100101 Firefox/61.0'}
    page = requests.get(url, headers = headers)
    while True:
        sleep(3)
        try:
            doc = html.fromstring(page.content)
            XPATH_NAME = '//h1[@id="title"]/span[@id="productTitle"]/text()'
            XPATH_SALE_PRICE =  '//div[@class="inlineBlock-display"]/span[2]/text()'
            XPATH_ORIGINAL_PRICE = '//span[@class="a-color-secondary a-text-strike"]/text()'
            XPATH_AVAILIBILITY = '//div[@id="availability"]/span/text()'

            RAW_NAME = doc.xpath(XPATH_NAME)
            RAW_SALE_PRICE = doc.xpath(XPATH_SALE_PRICE)
            RAW_ORIGINAL_PRICE = doc.xpath(XPATH_ORIGINAL_PRICE)
            RAW_AVAILIBILITY = doc.xpath(XPATH_AVAILIBILITY)

            NAME = ' '.join(''.join(RAW_NAME).split()) if RAW_NAME else None
            SALE_PRICE = ' '.join(''.join(RAW_SALE_PRICE).split()) if RAW_SALE_PRICE else None
            ORIGINAL_PRICE = ' '.join(''.join(RAW_ORIGINAL_PRICE).split()) if RAW_ORIGINAL_PRICE else None
            AVAILIBILITY = ' '.join(''.join(RAW_AVAILIBILITY).split()) if RAW_AVAILIBILITY else None

            if not ORIGINAL_PRICE:
                ORIGINAL_PRICE = SALE_PRICE

            if page.status_code != 200:
                raise ValueError('captha')

            data = {
                'NAME':NAME,
                'SALE_PRICE':SALE_PRICE,
                'ORIGINAL_PRICE':ORIGINAL_PRICE,
                'AVAILIBILITY':AVAILIBILITY
            }
            return data
        except Exception as e:
            print(e)

def ReadAsin():
    AsinList = [
        '/Girl-Wash-Your-Face-Believing/dp/1400201659/ref=zg_bs_books_1/142-8123915-1353401?_encoding=UTF8&psc=1&refRID=ZHAQHRV9K472FR5TSWN1',
        '/President-Missing-Novel-James-Patterson/dp/0316412694/ref=zg_bs_books_2?_encoding=UTF8&psc=1&refRID=C73GH6ZZP10JYYE4WZ79'
    ]
    extracted_data = []
    for i in AsinList:
        url = 'http://www.amazon.com' + i
        print('Processing ' + url)
        AmzonParse(url)
        extracted_data.append(AmzonParse(url))
        sleep(5)
    f = open('data.json', 'w')
    json.dump(extracted_data, f, indent=4)

if __name__ == '__main__':
    ReadAsin()