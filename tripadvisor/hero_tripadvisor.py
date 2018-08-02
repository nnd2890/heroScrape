from datetime import datetime
from time import time
from lxml import html
import requests, re
import os, sys
import unicodecsv as csv
import argparse

def parse(locality, checkin_date, checkout_date, sort):
    checkIn = checkin_date.strftime("%Y/%m/%d")
    checkOut = checkout_date.strftime("%Y/%m/%d")
    print("Scraper Inititated for Locality:%s"%locality)

    print("Finding search result page URL")
    geo_url = 'https://www.tripadvisor.com/TypeAheadJson?action=API&startTime='+str(int(time()))+'&uiOrigin=GEOSCOPE&source=GEOSCOPE&interleaved=true&types=geo,theme_park&neighborhood_geos=true&link_type=hotel&details=true&max=12&injectNeighborhoods=true&query='+locality
    api_response = requests.get(geo_url, verify=False).json()
    url_from_autocomplete = 'http://www.tripadvisor.com'+api_response['results'][0]['url']
    print("URL found %s"%url_from_autocomplete)
    geo = api_response['results'][0]['value']

    date = checkin_date.strftime("%Y_%m_%d") + "_" + checkout_date.strftime("%Y_%m_%d")
    form_data = {'changeSet': 'TRAVEL_INFO',
            'showSnippets': 'false',
            'staydates':date,
            'uguests': '2',
            'sortOrder':sort
    }
    headers = {
        'Accept': 'text/javascript, text/html, application/xml, text/xml, */*',
        'Accept-Encoding': 'gzip,deflate',
        'Accept-Language': 'en-US,en;q=0.5',
        'Cache-Control': 'no-cache',
        'Connection': 'keep-alive',
        'Content-Type': 'application/x-www-form-urlencoded; charset=utf-8',
        'Host': 'www.tripadvisor.com',
        'Pragma': 'no-cache',
        'Referer': url_from_autocomplete,
        'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:28.0) Gecko/20100101 Firefox/28.0',
        'X-Requested-With': 'XMLHttpRequest'
    }
    cookies = {"SetCurrency": "USD"}
    print("Downloading search results page")
    page_response = requests.post(url=url_from_autocomplete, data=form_data, headers=headers, cookies=cookies, verify=False)
    print("Parsing results")
    parser = html.fromstring(page_response.text)
    hotel_lists = parser.xpath('//div[contains(@class,"listItem")]//div[contains(@class,"listing collapsed")]')
    hotel_data = []
    if not hotel_lists:
        hotel_lists = parser.xpath('//div[contains(@class,"listItem")]//div[@class="listing"]')

    for hotel in hotel_lists:
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

        url = 'https://www.tripadvisor.com' + raw_hotel_link[0] if raw_hotel_link else None
        reviews = ''.join(raw_no_of_review).replace('reviews','').replace(',','') if raw_no_of_review else 0
        rank = ''.join(raw_rank) if raw_rank else None
        rating = ''.join(raw_rating).replace("of 5 bubbles", "").strip() if raw_rating else None
        hotel_name = ''.join(raw_hotel_name).strip() if raw_hotel_name else None
        hotel_features = ','.join(raw_hotel_features) if raw_hotel_features else None
        hotel_price = ''.join(raw_hotel_price).encode() if raw_hotel_price else None

        no_of_deals = re.findall("all\s+?(\d+)\s+?", "".join(raw_no_of_deals))
        if no_of_deals:
            no_of_deals = no_of_deals[0]
        else:
            no_of_deals = 0

        booking_provider = ''.join(raw_booking_provider).strip()

        data = {
            'url':url,
            'reviews':reviews,
            'rank':rank,
            'rating':rating,
            'hotel_name':hotel_name,
            'hotel_features':hotel_features,
            'hotel_price':hotel_price,
            'no_of_deals':no_of_deals,
            'booking_provider':booking_provider,
        }
        hotel_data.append(data)

    return hotel_data

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('checkin_date', help='Hotel check in date (format: YYYY/MM/DD)')
    parser.add_argument('checkout_date', help='Hotel check out date (format: YYYY/MM/DD)')
    sortorder_help="""
    available sort orders are: \n
    priceLow - hotels with lowest price,
    disLow: Hotel located near to search center,
    recommended: highest rated hotels based on traveler reviews,
    popularity: Most popular hotels as chosen Tripadvisor user
    """
    parser.add_argument('sort', help=sortorder_help, default='popularity')
    parser.add_argument('locality', help='Search Locality')
    args = parser.parse_args()
    locality = args.locality
    checkin_date = datetime.strptime(args.checkin_date, "%Y/%m/%d")
    checkout_date = datetime.strptime(args.checkout_date, "%Y/%m/%d")
    sort = args.sort
    checkIn = checkin_date.strftime("%Y/%m/%d")
    checkOut = checkout_date.strftime("%Y/%m/%d")
    today = datetime.now()

    if today<datetime.strptime(checkIn,"%Y/%m/%d") and datetime.strptime(checkIn,"%Y/%m/%d")<datetime.strptime(checkOut,"%Y/%m/%d"):
        data = parse(locality, checkin_date, checkout_date, sort)
        print("Writing to output file tripadvisor_data.csv")
        with open('tripadvisor_data.csv', 'wb') as csvfile:
            fieldnames = [
                'url',
                'reviews',
                'rank',
                'rating',
                'hotel_name',
                'hotel_features',
                'hotel_price',
                'no_of_deals',
                'booking_provider'
            ]

            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for row in data:
                writer.writerow(row)

    elif today>datetime.strptime(checkIn,"%Y/%m/%d") or today>datetime.strptime(checkOut,"%Y/%m/%d"):
        print("Invalid Checkin date: Please enter a valid checkin and checkout dates,entered date is already passed")
    elif datetime.strptime(checkIn, "%Y/%m/%d") > datetime.strptime(checkOut, "%Y/%m/%d"):
        print ("Invalid Checkin date: CheckIn date must be less than checkOut date")
