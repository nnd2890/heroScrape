import requests
from lxml import html
import unicodecsv as csv
from multiprocessing import Pool as ThreadPool, Manager, Process, Queue
from urllib.parse import urlparse
import re
import sys, os
from user_agent import generate_user_agent
import json
from mysql_database import MysqlDatabase
from mongodb_database import MongoDatabase

def parse(id_subur):
    url = 'https://www.keys2drive.com.au/find-an-instructor'
    headers = {'user-agent':generate_user_agent(os=('mac', 'linux'), device_type="desktop")}
    proxy = '1.54.213.202:80'
    proxies = {"http": "http://" + proxy, "https": "http://" + proxy}
    scraped_results = []
    try:
        cookie = {'XSRF-TOKEN': 'XSRF-TOKEN=eyJpdiI6IlVMbE42K056YVIxT1lISFpGeEhxRkE9PSIsInZhbHVlIjoiaDhVakRWdENMeVBtZ2ZQU3pVa25vQnM1NDhzcVRXZXR4aHpEdFBGMUx2bklWWVwvREpYdG5ocHZvZXpYNmlZQ2laemN5RjdTWkxKVzNQZFZRdTM1XC81QT09IiwibWFjIjoiYzcwNWI1NDFkZjk2ZGJjYzM4MmQ4ODM1NDZiM2M1NWE0ODc1MGE3MGJhNWFjZmNlM2YyMTIwZmUwMzNlYzEzOCJ9; laravel_session=eyJpdiI6IkE3ODZUYnNzTnF5c202MU9INGxyXC9nPT0iLCJ2YWx1ZSI6IkZrQzh4NEVvUktsMVJORWNPUmQ1TUpOMzg0eUt1SXZ3WityTjRqOHFiUlwvUWgrVkNFUjZNSU1cL29OeVpjUzExS0JiNVVzMHhNNWcxcGhMd3UwYWRNN1E9PSIsIm1hYyI6ImNlYjJkNzdlMTZhY2VlYWY2ZWUwZjZjMTJiOTNiNTUwNmYwZTRiMmE5YzBjMDYyMGUwYzFlZDI5N2JiNGZlMjAifQ%3D%3D'}
        formData = {
            '_token': 'qzyPnngx2GOJ9kfhO091KkDHdd5GI5FZw1tX3erk',
            'suburb_id': id_subur,
            'drive_school': '',
            'instructor': ''
        }
        response = requests.post(url, headers = headers, data=formData, cookies=cookie)
        print("Parsing page")
        if response.status_code == 200:
            print(url)

            parser = html.fromstring(response.text)
            list = parser.xpath('//table/tbody//tr')
            print(len(list))
            if len(list) > 1:
                for item in list:
                    XPATH_NAME = './td[1]//text()'
                    XPATH_DRIVE_SCHOOL = './td[2]//text()'
                    XPATH_PHONE = './td[3]//text()'
                    XPATH_MOBILE = './td[4]//text()'
                    XPATH_EMAIL = './td[5]//text()'
                    XPATH_WEBSITE = './td[6]//text()'
                    XPATH_STATE = './td[7]//text()'
                    XPATH_VEHICLE_TYPE = './td[8]//text()'
                    XPATH_AFFILIATIONS = './td[9]//text()'

                    name = get_string(item,XPATH_NAME)
                    dirve_school = get_string(item,XPATH_DRIVE_SCHOOL)
                    phone = get_string(item,XPATH_PHONE)
                    mobile = get_string(item,XPATH_MOBILE)
                    email = get_string(item,XPATH_EMAIL)
                    website = get_string(item,XPATH_WEBSITE)
                    state = get_string(item,XPATH_STATE)
                    vehicle_type = get_string(item,XPATH_VEHICLE_TYPE)
                    affiliations = get_string(item,XPATH_AFFILIATIONS)

                    data = {
                        'name': name,
                        'dirve_school': dirve_school,
                        'phone': phone,
                        'mobile': mobile,
                        'email': email,
                        'website': website,
                        'state': state,
                        'vehicle_type': vehicle_type,
                        'affiliations': affiliations,
                    }
                    scraped_results.append(data)
                # print(scraped_results)
                return scraped_results
            else:
                return []
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
            if datas:
                for data in datas:
                    writer.writerow(data)
    print("Writing %s.csv Finished!" % name_file)


def writeJsonFile(name_file, scraped_data):
    print("Writing scraped data to %s.json" % name_file)
    with open('%s.json' % name_file, 'w') as jsonfile:
        jsonData = []
        for datas in scraped_data:
            if datas:
                for data in datas:
                    jsonData.append(data)
        json.dump(jsonData, jsonfile, indent=4)
    print("Writing %s.json Finished!" % name_file)

def get_all_suburs(url):
    headers = {'user-agent': generate_user_agent(os=('mac', 'linux'), device_type="desktop")}
    proxy = '1.54.213.202:80'
    proxies = {"http": "http://" + proxy, "https": "http://" + proxy}
    scraped_results = []
    response = requests.get(url, headers=headers).json()
    results = response['results']
    subur_database = MysqlDatabase()

    for result in results:
        id = result['id']
        text = result['text']
        subur = {}
        subur['id_suburbs'] = id
        subur['name_suburbs'] = text
        subur['url'] = url
        subur_database.insertRow("suburs", subur)

def save_subur_to_database():
    url_list = []
    url_append = 'https://www.keys2drive.com.au/suburbs/select2_list?page='
    for i in range(2,1500):
        url_list.append(url_append + str(i))
    pool = ThreadPool(4)
    pool.map(get_all_suburs, url_list)

def get_all_idsuburs():
    id_suburs = []
    subur_database = MysqlDatabase()
    results = subur_database.selectField('suburs', 'id_suburbs')
    for result in results:
        id_suburs.append(result[0])
    return id_suburs

if __name__=="__main__":

    id_suburs = get_all_idsuburs()
    print(id_suburs)


    # Make the Pool of workers
    pool = ThreadPool(4)
    # Open the urls in their own threads and return the results
    scraped_data = pool.map(parse, id_suburs)
    # Close the pool and wait for the work to finish
    pool.terminate()
    pool.join()

    print(scraped_data)
    name_file = "key2drive_example"
    fieldnames = [
        'name',
        'dirve_school',
        'phone',
        'mobile',
        'email',
        'website',
        'state',
        'vehicle_type',
        'affiliations'
    ]

    # writeJsonFile(name_file, scraped_data)
    writeCsvFile(name_file, fieldnames, scraped_data)

    # sql = Database()
    # sql.mySql(scraped_data)

    # mongodb = MongoDatabase()
    # mongodb.insertList(scraped_data[0])



