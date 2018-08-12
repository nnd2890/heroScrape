from lxml import html
import requests
import re
import os
import sys
import unicodecsv as csv
import argparse
import json

def parse(keyword, place):
    headers = {'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
               'accept-encoding': 'gzip, deflate, sdch, br',
               'accept-language': 'en-GB,en-US;q=0.8,en;q=0.6',
               'referer': 'https://www.glassdoor.com/',
               'upgrade-insecure-requests': '1',
               'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/51.0.2704.79 Chrome/51.0.2704.79 Safari/537.36',
               'Cache-Control': 'no-cache',
               'Connection': 'keep-alive'
               }

    location_headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.01',
        'accept-encoding': 'gzip, deflate, sdch, br',
        'accept-language': 'en-GB,en-US;q=0.8,en;q=0.6',
        'referer': 'https://www.glassdoor.com/',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/51.0.2704.79 Chrome/51.0.2704.79 Safari/537.36',
        'Cache-Control': 'no-cache',
        'Connection': 'keep-alive'
    }
    data = {"term": place,
            "maxLocationsToReturn": 10}

    location_url = "https://www.glassdoor.co.in/findPopularLocationAjax.htm?"

    try:
        print("Fetching loaction details")
        location_response = requests.post(location_url, headers=headers, data=data).json()
        print(location_response)
    except:
        print("Failed to load locations")



if __name__=="__main__":
    """
        eg-:python 1934_glassdoor.py "Android developer", "new york"
    """

    argparser = argparse.ArgumentParser()
    argparser.add_argument('keyword', help='job name', type=str)
    argparser.add_argument('place', help='job location', type=str)
    args = argparser.parse_args()
    keyword = args.keyword
    place = args.place
    print("Fetching job details")
    scraped_data = parse(keyword, place)
    print("Writing data to output file")

    # with open('%s-%s-job-results.csv' %(keyword, place), "wb") as csvfile:
    #     fieldnames = ['Name', 'Company', 'State',
		# 			  'City', 'Salary', 'Location', 'Url']
    #     writer = csv.DictWriter(csvfile, fieldnames = fieldnames, quoting = csv.QUOTE_ALL)
    #     writer.writeheader()
    #     if scraped_data:
    #         for data in scraped_data:
    #             writer.writerow(data)
    #     else:
    #         print("You search for %s, in %s does not match any jobs"%(keyword, place))