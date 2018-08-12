from lxml import html
import requests
from collections import OrderedDict
import json
import argparse
import re

def parse(url):
    print('Fetching %s'%url)
    response = requests.get(url)
    parser = html.fromstring(response.text)

    XPATH_RATING = '//div[contains(@class, "noncollapsible")]//div[contains(@class, "choices")]//div[contains(@class, "ui_checkbox item")]'
    ratings = parser.xpath(XPATH_RATING)
    ratings_dict = OrderedDict()
    for rating in ratings:
        XPATH_RATING_KEY = './/label[contains(@class, "row_label")]//text()'
        XPATH_RATING_VALUE = './/span[contains(@class, "row_num")]//text()'

        raw_rating_key = rating.xpath(XPATH_RATING_KEY)
        raw_rating_value = rating.xpath(XPATH_RATING_VALUE)

        cleaned_rating_key = ''.join(raw_rating_key)
        cleaned_rating_value = ''.join(raw_rating_value).replace(',','') if raw_rating_value else 0
        ratings_dict.update({cleaned_rating_key:int(cleaned_rating_value)})

    XPATH_NAME = '//h1[@id="HEADING"]//text()'
    raw_name = parser.xpath(XPATH_NAME)
    name = get_string(raw_name)

    XPATH_HOTEL_RATING = '//span[@property="ratingValue"]//@content'
    raw_rating = parser.xpath(XPATH_HOTEL_RATING)
    hotel_rating =  get_string(raw_rating)

    XPATH_REVIEWS = '//a[contains(@class, "seeAllReviews")]//text()'
    raw_review_count = parser.xpath(XPATH_REVIEWS)
    view_count = get_number(raw_review_count)

    XPATH_RANK = '//span[contains(@class,"popularity")]//text()'
    raw_rank = parser.xpath(XPATH_RANK)
    rank = get_string(raw_rank)

    XPATH_STREET_ADDRESS = '//span[@class="street-address"]/text()'
    raw_rank = parser.xpath(XPATH_STREET_ADDRESS)
    address = get_string(raw_rank)

    XPATH_LOCALITY = '//span[contains(@class, "locality")]//text()'
    raw_locality = parser.xpath(XPATH_LOCALITY)[0]
    locality = get_string(raw_locality)
   
    XPATH_AMENITIES = '//div[contains(text(), "Amenities")]/following-sibling::div[1]//div[@class!="textitem"]'
    amenities = parser.xpath(XPATH_AMENITIES)
    amenity_dict = OrderedDict()
    for amenity in amenities:
        XPATH_AMENITY_KEY = './/div[contains(@class, "sub_title")]//text()'
        XPATH_AMENITY_VALUE = './/div[contains(@class, "sub_content")]//text()'

        raw_amenity_key = parser.xpath(XPATH_AMENITY_KEY)
        raw_amenity_value = parser.xpath(XPATH_AMENITY_VALUE)
        if raw_amenity_key and raw_amenity_value:
            amenity_key = get_string(raw_amenity_key)
            amenity_value = get_string(raw_amenity_value)
            amenity_dict.update({amenity_key:amenity_value})
        

    XPATH_HIGHLIGHTS = '//div[contains(@class, "highlightedAmenity")]//text()'
    raw_highlights = parser.xpath(XPATH_HIGHLIGHTS)
    cleaned_highlights = filter(lambda x:x != '\n', raw_highlights)
    highlights = get_string(cleaned_highlights)

    

    XPATH_ADDITIONAL_INFO = '//div[contains(text(), "Details")]/following-sibling::div[@class="selection_content"]/div'
    raw_additional_info = parser.xpath(XPATH_ADDITIONAL_INFO)
    additional_info_dict = OrderedDict()
    for info in raw_additional_info:
        XPATH_INFO_TEXT = "./text()"
        if info.xpath(XPATH_INFO_TEXT):
            XPATH_INFO_KEY = ".//text()"
            XPATH_INFO_VALUE = "./following-sibling::div[1]//text()"

            raw_info_key = info.xpath(XPATH_INFO_KEY)
            raw_info_value = info.xpath(XPATH_INFO_VALUE)
            if raw_info_value and raw_info_key:
                # cleaning
                raw_info_value = ''.join(raw_info_value).replace("#", ", #").lstrip(", ")
                if raw_info_key[0] == "Hotel class":
                    continue
                additional_info_dict.update({raw_info_key[0]: raw_info_value})

    XPATH_FULL_ADDRESS_JSON = '//script[@type="application/ld+json"]//text()'
    raw_full_address_json = parser.xpath(XPATH_FULL_ADDRESS_JSON)
    if raw_full_address_json:
        try:
            parsed_address_info = json.loads(raw_full_address_json[0])
            zipcode = parsed_address_info['address'].get('postalCode')
            country = parsed_address_info['address'].get('addressCountry', {}).get('name')

        except Exception as e:
            raise e













    print (parsed_address_info)
    return ''

def get_string(arr):
    str = ''.join(arr).strip() if arr else None
    return str

def get_number(arr):
    if arr:
        str = get_string(arr)
        number = re.findall(r'\d+[,.]?\d+', str)[0].replace(',','')
        return number
    else:
        return None
    

if __name__=='__main__':
	parser = argparse.ArgumentParser()
	parser.add_argument('url',help='Tripadvisor hotel url')
	args = parser.parse_args()
	url = args.url
	scraped_data = parse(url)
    # with open('tripadvisor_hotel_scraped_data.json', 'w') as f:
    #     json.dump(scraped_data, f, indent=4, ensure_ascii=False)