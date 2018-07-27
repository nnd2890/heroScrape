import requests
from lxml import html
import unicodecsv as csv
from multiprocessing import Pool as ThreadPool
from urllib.parse import urlparse
import re
import sys, os
from user_agent import generate_user_agent


def parse_listing(url):
    headers = generate_user_agent(os=('mac', 'linux'), device_type="desktop")
    scraped_results = []
    try:
        response = requests.get(url, verify=False, headers = headers)
        print("Parsing page")
        if response.status_code == 200:
            print(url)
            parser = html.fromstring(response.text)

            PRODUCT_NAME_XPATH = '//*[@id="productTitle"]'
            ORIGINAL_PRICE_XPATH = ''
            SALE_PRICE_XPATH = '//*[@id="price_inside_buybox"]'
            AVAILABILITY_XPATH = '//*[@id="availability"]/span'

            product_name = ''
            original_price = ''
            sale_price = ''
            availability = ''

            details = {
                'product_name':product_name,
                'original_price' :original_price,
                'sale_price' :sale_price,
                'availability' :availability,
                'url' :url
            }
            scraped_results.append(details)
            break
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
    print(scraped_results)
    return scraped_results

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

if __name__=="__main__":
    page_numbers = range(1, 50)
    search_url = 'https://www.menulog.com.au/area/3057-brunswick-east'
    url_list = [search_url]

    # Make the Pool of workers
    pool = ThreadPool(10)
    # Open the urls in their own threads and return the results
    scraped_data = pool.map(parse_listing, url_list)
    # Close the pool and wait for the work to finish
    pool.terminate()
    pool.join()

    if scraped_data:
        name_file = "menulog_business_details"
        print("Writing scraped data to %s.csv" %name_file)
        with open('%s.csv' %name_file, 'wb') as csvfile:
            fieldnames = [
                'business_name',
                'rating',
                'categories',
                'address',
                'url'
            ]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames,quoting=csv.QUOTE_ALL)
            writer.writeheader()
            for datas in scraped_data:
                for data in datas:
                    writer.writerow(data)
        print("Finished!")