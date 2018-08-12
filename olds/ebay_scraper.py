import requests
from lxml import html
import unicodecsv as csv
from multiprocessing import Pool as ThreadPool


def parse_listing(url):
    headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'}
    proxy = '167.99.157.10:3128'
    proxies = {"http": "http://" + proxy,
                "https": "http://" + proxy}
    scraped_results = []
    try:
        response = requests.get(url, verify=False, headers = headers)
        if response.status_code == 200:
            print("Parsing page:", url)
            parser = html.fromstring(response.text)

            base_url = "https://www.ebay.com"
            parser.make_links_absolute(base_url)

            LISTINGS_XPATH = '//li[@class="s-item"]'
            listings = parser.xpath(LISTINGS_XPATH)
            for results in listings[1:4]:
                URL_XPATH = './/a[@class="s-item__link"]/@href'
                TITLE_XPATH = './/a[@class="s-item__link"]/h3[@class="s-item__title"]/text()'
                PRICE_XPATH = './/span[@class="s-item__price"]//text()'


                url = get_string(results, URL_XPATH)
                title = get_string(results, TITLE_XPATH)
                price = get_string(results, PRICE_XPATH)

                details = {
                    'url':url,
                    'title':title,
                    'price':price
                }

                scraped_results.append(details)
        elif response.status_code == 404:
            print("Could not find a location matching", response.status_code)
            return []
        else:
            print("Failed to process page", response.status_code)
            return []
    except:
        print("Failed to process page")
        return []
    return scraped_results

def get_string(parser, XPATH):
    arr = parser.xpath(XPATH)
    str = ''.join(arr).strip() if arr else None
    return str

def get_number(arr):
    if arr:
        str = get_string(arr)
        number = re.findall(r'\d+[,.]?\d+', str)[0].replace(',','')
        return number
    else:
        return None

if __name__=="__main__":
    page_numbers = range(1, 2)
    search_url = 'https://www.ebay.com/sch/i.html?_from=R40&_sacat=0&_nkw=iphone+7&_blrs=recall_filtering&_pgn='
    url_list = [search_url + str(i) for i in page_numbers]

    # Make the Pool of workers
    pool = ThreadPool(10)
    # Open the urls in their own threads and return the results
    scraped_data = pool.map(parse_listing, url_list)
    # Close the pool and wait for the work to finish
    pool.terminate()
    pool.join()

    print(scraped_data)

    if scraped_data:
        file_name = 'iphone7-ebay-scraped-data.csv'
        print("Writing scraped data to", file_name)
        with open(file_name, 'wb') as csvfile:
            fieldnames = [
                'business_name',
                'business_page',
                'telephone',
                'street_address',
                'locality',
                'region',
                'postal_code',
                'rank'
            ]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames,quoting=csv.QUOTE_ALL)
            writer.writeheader()
            for datas in scraped_data:
                for data in datas:
                    writer.writerow(data)
        print("Finished!")