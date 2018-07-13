from lxml import html
import json
import requests
from time import sleep
import re, urllib, urllib.parse
import argparse

def parse(url):
    headers={
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'
    }
    response = requests.get(url, headers=headers, verify=False).text
    parser = html.fromstring(response)
    print('Parsing the page')
    raw_name = parser.xpath('//h1[contains(@class,"biz-page-title")]//text()')
    raw_claimed = parser.xpath('//span[contains(@class,"claim-status_icon--claimed")]/parent::div/text')
    raw_reviews = parser.xpath('//div[contains(@class,"biz-main-info")]//span[contains(@class,"review-count rating-qualifier")]//text()')
    raw_category = parser.xpath('//div[contains(@class,"biz-page-header")]//span[contains(@class,"category-str-list")]//a//text()')
    hours_table = parser.xpath('//table[contains(@class,"hours-table")]//tr')
    details_table = parser.xpath('//div[contains(@class,"short-def-list")]//dl')
    raw_map_link = parser.xpath('//a[contains(@class,"biz-map-directions")]/img/@src')
    raw_phone = parser.xpath('//span[contains(@class,"biz-phone")]//text()')
    raw_address = parser.xpath('//div[contains(@class,"mapbox-text")]//div[contains(@class,"map-box-address")]//text()')
    raw_wbsite_link = parser.xpath('//span[contains(@class,"biz-website")]/a/@href')
    raw_price_range = parser.xpath('//dd[contains(@class,"price-description")]//text()')
    raw_health_rating = parser.xpath('//dd[contains(@class,"health-score-description")]//text()')
    rating_histogram = parser.xpath('//table[contains(@class,"histogram")]//tr[contains(@class,"histogram_row")]')
    raw_ratings = parser.xpath('//div[contains(@class,"biz-main-info")]//div[contains(@class,"i-stars")]/@title')

    working_hours = []
    for hours in hours_table:
        raw_day = hours.xpath('.//th//text()')
        raw_timing = hours.xpath('./td//text()')
        day = ''.join(raw_day).strip()
        timing = ''.join(raw_timing).strip()
        working_hours.append({day:timing})
    
    infor = []
    for details in details_table:
        raw_description_key = details.xpath('.//dt//text()')
        raw_description_value = details.xpath('.//dd/text()')
        description_key = ''.join(raw_description_key).strip()
        description_value = ''.join(raw_description_value).strip()
        infor.append({description_key:description_value})

    ratings_histogram = []
    for ratings in rating_histogram:
        raw_rating_key = details.xpath('.//th//text()')
        raw_rating_value = details.xpath('.//td[@class="histogram_count"]/text()')
        rating_key = ''.join(raw_rating_key).strip()
        rating_value = ''.join(raw_rating_value).strip()
        infor.append({rating_key:rating_value})


    name = ''.join(raw_name).strip()
    phone = ''.join(raw_phone).strip()
    address = ''.join(raw_address).strip()
    health_rating = ''.join(raw_health_rating).strip()
    price_range = ''.join(raw_price_range).strip()
    claimed_status = ''.join(raw_claimed).strip()
    reviews = ''.join(raw_reviews).strip()
    category = ''.join(raw_category).strip()
    cleaned_ratings = ''.join(raw_ratings).strip()

    if raw_wbsite_link:
        decoded_raw_website_link = urllib.parse.unquote(raw_wbsite_link[0])
        website = decoded_raw_website_link
    else:
        website = ''

    if raw_map_link:
        decoded_map_url = urllib.parse.unquote(raw_map_link[0])
        map_coordinates = decoded_map_url
        latitude = map_coordinates[0]
        longtitude = map_coordinates[1]
    else:
        latitude = ''
        longtitude = ''

    if raw_ratings:
        ratings = re.findall("\d+[.,]?\d+", cleaned_ratings)[0]
    else:
        ratings = 0

    data = {
        'working_hours':working_hours,
        'infor':infor,
        'name':name,
        'phone':phone,
        'ratings':ratings,
        'address':address,
        'health_rating':health_rating,
        'price_range':price_range,
        'claimed_status':claimed_status,
		'reviews':reviews,
		'category':category,
		'website':website,
		'latitude':latitude,
		'longtitude':longtitude,
		'url':url
    }

    return data

if __name__=="__main__":
    argparse = argparse.ArgumentParser()
    argparse.add_argument('url', help='yelp bussiness url')
    args = argparse.parse_args()
    url = args.url
    parse(url)
    scraped_data = parse(url)
    yelp_id = url.split('/')[-1]
    with open('scraped_data-%s.json'%(yelp_id),'w') as fp:
        json.dump(scraped_data, fp, indent=4)