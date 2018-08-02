import requests
from lxml import html
import unicodecsv as csv
from multiprocessing import Pool as ThreadPool
from urllib.parse import urlparse
import re
import sys, os
from user_agent import generate_user_agent
import json
from mysql_database import Database
from mongodb_database import MongoDatabase

def parse(url):
    headers = {'user-agent':generate_user_agent(os=('mac', 'linux'), device_type="desktop")}
    proxy = '1.54.213.202:80'
    proxies = {"http": "http://" + proxy, "https": "http://" + proxy}
    scraped_results = []
    try:
        response = requests.get(url, headers = headers)
        print("Parsing page")
        print(response.cookies)
        if response.status_code == 200:
            print(url)

            parser = html.fromstring(response.text)
            list = parser.xpath('//div[contains(@class, "listItem")]')

            for hotel in list:
                XPATH_HOTEL_LINK = './/a[contains(@class, "property_title")]/@href'
                XPATH_REVIEWS = './/a[contains(@class, "review_count")]//text()'
                XPATH_RANK = './/div[contains(@class, "popindex")]//text()'
                XPATH_RATING = './/span[contains(@class,"rating")]//@alt'
                XPATH_HOTEL_NAME = './/a[contains(@class, "property_title")]/text()'
                XPATH_HOTEL_FEATURES = './/div[contains(@class,"common_hotel_icons_list")]//li//text()'
                XPATH_HOTEL_PRICE = './/div[contains(@data-sizegroup,"mini-meta-price")]/text()'
                XPATH_VIEW_DEALS = './/div[contains(@data-ajax-preserve,"viewDeals")]//text()'
                XPATH_BOOKING_PROVIDER = './/div[contains(@data-sizegroup,"mini-meta-provider")]//text()'

                raw_hotel_link = hotel.xpath(XPATH_HOTEL_LINK)
                raw_no_of_review = hotel.xpath(XPATH_REVIEWS)
                raw_rank = hotel.xpath(XPATH_RANK)
                raw_rating = hotel.xpath(XPATH_RATING)
                raw_hotel_name = hotel.xpath(XPATH_HOTEL_NAME)
                raw_hotel_features = hotel.xpath(XPATH_HOTEL_FEATURES)
                raw_hotel_price = hotel.xpath(XPATH_HOTEL_PRICE)
                raw_no_of_deals = hotel.xpath(XPATH_VIEW_DEALS)
                raw_booking_provider = hotel.xpath(XPATH_BOOKING_PROVIDER)

                hotel_url = 'https://www.tripadvisor.com' + raw_hotel_link[0] if raw_hotel_link else None
                reviews = ''.join(raw_no_of_review).replace('reviews', '').replace(',', '') if raw_no_of_review else 0
                rank = ''.join(raw_rank) if raw_rank else None
                rating = ''.join(raw_rating).replace("of 5 bubbles", "").strip() if raw_rating else None
                hotel_name = ''.join(raw_hotel_name).strip() if raw_hotel_name else None
                hotel_features = ','.join(raw_hotel_features) if raw_hotel_features else None
                hotel_price = ''.join(raw_hotel_price) if raw_hotel_price else None

                no_of_deals = re.findall("all\s+?(\d+)\s+?", "".join(raw_no_of_deals))
                if no_of_deals:
                    no_of_deals = no_of_deals[0]
                else:
                    no_of_deals = 0

                booking_provider = ''.join(raw_booking_provider).strip()

                data = {
                    'url': url,
                    'reviews': reviews,
                    'rank': rank,
                    'rating': rating,
                    'hotel_name': hotel_name,
                    'hotel_features': hotel_features,
                    'hotel_price': hotel_price,
                    'no_of_deals': no_of_deals,
                    'booking_provider': booking_provider,
                    'hotel_url':hotel_url
                }
                scraped_results.append(data)
            # print(scraped_results)
            return scraped_results

        elif response.status_code == 404:
            print("Could not find a location matching", response.status_code)
            return []

        else:
            print("Failed to process page", response.status_code)
            return []

    except Exception as e:
        print("Failed to process page:", e)
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(exc_type, fname, exc_tb.tb_lineno)
        return []

def get_string(parser, XPATH):
    arr = parser.xpath(XPATH)
    str = ''.join(arr).strip() if arr else None
    return str

def get_number(parser, XPATH):
    arr = parser.xpath(XPATH)
    str = ''.join(arr).strip() if arr else None
    number = re.findall(r'\d+[,.]?\d+', str)[0] if str else None
    return number

def is_absolute_url(url):
    return bool(urlparse(url).netloc)

def writeCsvFile(name_file, fieldnames, scraped_data):
    print("Writing scraped data to %s.csv" % name_file)
    with open('%s.csv' % name_file, 'wb') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames, quoting=csv.QUOTE_ALL)
        writer.writeheader()
        for datas in scraped_data:
            for data in datas:
                writer.writerow(data)
    print("Writing %s.csv Finished!" % name_file)


def writeJsonFile(name_file, scraped_data):
    print("Writing scraped data to %s.json" % name_file)
    with open('%s.json' % name_file, 'w') as jsonfile:
        jsonData = []
        for datas in scraped_data:
            for data in datas:
                jsonData.append(data)
        json.dump(jsonData, jsonfile, indent=4)
    print("Writing %s.json Finished!" % name_file)


if __name__=="__main__":
    page_numbers = range(1, 7)
    url_list = []
    for page in page_numbers:
        paginate = page*30 - 30
        search_url = 'https://www.tripadvisor.com/Hotels-g60745-oa' + str(paginate) + '-Boston_Massachusetts-Hotels.html'
        url_list.append(search_url)

    print(url_list)

    # Make the Pool of workers
    pool = ThreadPool(10)
    # Open the urls in their own threads and return the results
    scraped_data = pool.map(parse, url_list)
    # Close the pool and wait for the work to finish
    pool.terminate()
    pool.join()

    if scraped_data:
        name_file = "my_tripadvisor"
        fieldnames = [
            'url',
            'reviews',
            'rank',
            'rating',
            'hotel_name',
            'hotel_features',
            'hotel_price',
            'no_of_deals',
            'booking_provider',
            'hotel_url'
        ]

        # writeJsonFile(name_file, scraped_data)
        # writeCsvFile(name_file, fieldnames)

        # sql = Database()
        # sql.mySql(scraped_data)

        # mongodb = MongoDatabase()
        # mongodb.insertList(scraped_data[0])



