import requests
from lxml import html
import unicodecsv as csv
from multiprocessing import Pool as ThreadPool
from urllib.parse import urlparse
import re
import sys, os


def parse_listing(url):
    headers = {
               'User-Agent': 'ozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'
               }
    scraped_results = []
    try:
        response = requests.get(url, verify=False, headers = headers)
        print("parsing page")
        if response.status_code == 200:
            print(url)
            parser = html.fromstring(response.text)

            base_url = "https://www.menulog.com"
            parser.make_links_absolute(base_url)

            LISTINGS_XPATH = '//*[@id="searchResults"]//section[@class="listing-item"]'
            listings = parser.xpath(LISTINGS_XPATH)
            for results in listings:
                BUSINESS_NAME_XPATH = './/h3[@class=" listing-item-title"]//text()'
                RATING_XPATH = './/span[contains(@class, "rating-stars-fill")]//text()'
                CATEGORY_XPATH = './/p[contains(@class,"infoText--primary")]//text()'
                ADDRESS_XPATH = './/p[contains(@itemprop,"address")]//text()'
                URL_XPATH = './/a[contains(@class,"mediaElement")]//@href'


                business_name = get_string(results, BUSINESS_NAME_XPATH)
                rating = get_string(results, RATING_XPATH)
                rating = re.findall(r'\d+[,.]?\d+', rating) if rating else None
                if not rating:
                    rating = 0
                else:
                    rating = rating[0]

                categories = get_string(results, CATEGORY_XPATH)
                address = get_string(results, ADDRESS_XPATH)
                url = get_string(results, URL_XPATH)

                business_details = {
                    'business_name':business_name,
                    'rating' :rating,
                    'categories' :categories,
                    'address' :address,
                    'url' :url
                }
                print(business_details)

                scraped_results.append(business_details)
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