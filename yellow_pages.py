import requests
from lxml import html
import unicodecsv as csv
import argparse

def parse_listing(keyword,place):
    url = "https://www.yellowpages.com/search?search_terms={0}&geo_location_terms={1}".format(keyword,place)
    headers = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
               'Accept-Encoding': 'gzip, deflate, br',
               'Accept-Language': 'en-GB,en;q=0.9,en-US;q=0.8,ml;q=0.7',
               'Cache-Control': 'max-age=0',
               'Connection': 'keep-alive',
               'Host': 'www.yellowpages.com',
               'Upgrade-Insecure-Requests': '1',
               'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36'
               }
    for retry in range(1):
        try:
            response = requests.get(url, verify=False, headers = headers)
            print("parsing page")
            if response.status_code == 200:
                parser = html.fromstring(response.text)

                base_url = "https://www.yellowpages.com"
                parser.make_links_absolute(base_url)

                XPATH_LISTINGS = '//div[@class="search-results organic"]//div[@class="v-card"]'
                listings = parser.xpath(XPATH_LISTINGS)
                scraped_results = []
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
                return scraped_results
            elif response.status_code == 404:
                print("Could not find a location matching", place)
                break
            else:
                print("Failed to process page", response.status_code)
                return []
        except:
            print("Failed to process page")
            return []

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
    argparser = argparse.ArgumentParser()
    argparser.add_argument('keyword', help='Search Keyword')
    argparser.add_argument('place', help='Place Name')

    args = argparser.parse_args()
    keyword = args.keyword
    place = args.place
    scraped_data = parse_listing(keyword, place)
    if scraped_data:
        print("Writing scraped data to %s-%s-yellowpages-scraped-data.csv"%(keyword,place))
        with open('%s-%s-yellowpages-scraped-data.csv', 'wb') as csvfile:
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
            for data in scraped_data:
                writer.writerow(data)