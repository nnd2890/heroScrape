import requests
from lxml import html
import unicodecsv as csv
from multiprocessing import Pool as ThreadPool


def parse_listing(url):
    headers = {
               'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36'
               }
    scraped_results = []
    try:
        response = requests.get(url, verify=False, headers = headers)
        print("parsing page")
        print(url)
        if response.status_code == 200:
            parser = html.fromstring(response.text)

            base_url = "https://www.yellowpages.com"
            parser.make_links_absolute(base_url)

            XPATH_LISTINGS = '//div[@class="search-results organic"]//div[@class="v-card"]'
            listings = parser.xpath(XPATH_LISTINGS)
            for results in listings:
                XPATH_BUSINESS_NAME = './/a[@class="business-name"]//text()'
                XPATH_BUSINESS_PAGE = './/a[@class="business-name"]//@href'
                XPATH_TELEPHONE = './/div[@itemprop="telephone"]/text()'
                XPATH_ADDRESS = './/p[@class="adr"]//span[@itemprop="streetAddress"]//text()'
                LOCALITY_XPATH = './/p[@class="adr"]//span[@itemprop="addressLocality"]//text()'
                REGION_XPATH = './/p[@class="adr"]//span[@itemprop="addressRegion"]//text()'
                POSTAL_CODE_XPATH = './/p[@class="adr"]//span[@itemprop="postalCode"]//text()'
                RANK_XPATH = './/div[@class="info"]//h2[@class="n"]/text()'

                business_name = get_string(results, XPATH_BUSINESS_NAME)
                business_page = get_string(results, XPATH_BUSINESS_PAGE)
                telephone = get_string(results, XPATH_TELEPHONE)
                street_address = get_string(results, XPATH_ADDRESS)
                locality = get_string(results, LOCALITY_XPATH).replace(r',', '')
                region = get_string(results, REGION_XPATH)
                postal_code = get_string(results, POSTAL_CODE_XPATH)
                rank = get_string(results, RANK_XPATH).replace(r'.', '')

                business_details = {
                    'business_name':business_name,
                    'business_page':business_page,
                    'telephone':telephone,
                    'street_address':street_address,
                    'locality':locality,
                    'region':region,
                    'postal_code':postal_code,
                    'rank':rank
                }

                scraped_results.append(business_details)
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
    page_numbers = range(1, 50)
    search_url = 'https://www.yellowpages.com/search?search_terms=restaurant&geo_location_terms=Boston, MA&page='
    url_list = [search_url + str(i) for i in page_numbers]

    # Make the Pool of workers
    pool = ThreadPool(10)
    # Open the urls in their own threads and return the results
    scraped_data = pool.map(parse_listing, url_list)
    # Close the pool and wait for the work to finish
    pool.terminate()
    pool.join()

    if scraped_data:
        print("Writing scraped data to yellowpages-scraped-data3.csv")
        with open('yellowpages-scraped-data4.csv', 'wb') as csvfile:
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