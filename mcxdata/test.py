import requests
from lxml import html
import unicodecsv as csv
from multiprocessing import Pool as ThreadPool
import re
import sys, os
import json
import time

def parse_listing(url):
    headers = {
               'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36'
               }

    proxy = '43.249.143.89:31191'
    proxies = {"http": "http://" + proxy, "https": "http://" + proxy}

    scraped_results = []
    try:
        response = requests.get(url, verify=False, headers = headers, proxies=proxies)
        print("parsing page")
        print(url)
        if response.status_code == 200:
            parser = html.fromstring(response.text)

            XPATH_LISTINGS = '//tbody//tr[@id]'
            listings = parser.xpath(XPATH_LISTINGS)
            for results in listings:
                XPATH_Commodity = './/td[1]//text()'
                XPATH_Price = './/td[2]//text()'
                XPATH_Chg = './/td[3]//text()'
                XPATH_percentChg = './/td[4]//text()'
                XPATH_Open = './/td[5]//text()'
                XPATH_High = './/td[6]//text()'
                XPATH_Low = './/td[7]//text()'
                XPATH_Time = './/td[8]//text()'

                Commodity = get_string(results, XPATH_Commodity)
                Price = get_string(results, XPATH_Price)
                Chg = get_string(results, XPATH_Chg)
                percentChg = get_string(results, XPATH_percentChg)
                Open = get_string(results, XPATH_Open)
                High = get_string(results, XPATH_High)
                Low = get_string(results, XPATH_Low)
                Time = get_string(results, XPATH_Time)

                POS = max(float(percentChg), (float(Price)-float(Low))/float(Price))
                NEG = min(float(percentChg), (float(Price)-float(Low))/float(Price))
                POS = round(POS, 2)
                NEG = round(NEG, 2)


                business_details = {
                    'Commodity':Commodity,
                    'Price':Price,
                    'Chg':Chg,
                    '%Chg':percentChg,
                    'Open':Open,
                    'High':High,
                    'Low':Low,
                    'Time':Time,
                    'POS':POS,
                    'NEG':NEG
                }

                scraped_results.append(business_details)
            # print(scraped_results)
            return  scraped_results
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

def get_number(arr):
    if arr:
        str = get_string(arr)
        number = re.findall(r'\d+[,.]?\d+', str)[0].replace(',','')
        return number
    else:
        return None

def writeCsvFile(name_file, fieldnames, scraped_data):
    print("Writing scraped data to %s.csv" % name_file)
    with open('%s.csv' % name_file, 'wb') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames, quoting=csv.QUOTE_ALL)
        writer.writeheader()
        for datas in scraped_data:
            if datas:
                for data in datas:
                    POS = data['POS']
                    NEG = data['NEG']
                    if (POS >= 1 or NEG <= -1):
                        writer.writerow(data)
    print("Writing %s.csv Finished!" % name_file)

def notify(notification_title, notification_message):
    api_key = 'DKG8TZBUJTZF53AOHIFDFJL88'
    # api_key = 'HNJZA120JIFFARA2O9H18MSV8'
    url = "https://www.notifymydevice.com/push"
    data = {"ApiKey": api_key, "PushTitle": notification_title, "PushText": notification_message}
    headers = {'Content-Type': 'application/json'}
    r = requests.post(url, data=json.dumps(data), headers=headers)
    if r.status_code == 200:
        print('Notification sent!')
    else:
        print('Error while sending notificaton!')

if __name__=="__main__":
    page_numbers = range(1, 50)
    url1 = 'http://www.mcxdata.in/livemcx.aspx'
    url2 = 'http://www.mcxdata.in/livencdex.aspx'
    url_list = []
    url_list.append(url1)
    url_list.append(url2)
    i = 1
    while True:
        # Code executed here
        # Make the Pool of workers
        pool = ThreadPool(10)
        # Open the urls in their own threads and return the results
        scraped_data = pool.map(parse_listing, url_list)
        # Close the pool and wait for the work to finish
        pool.terminate()
        pool.join()

        name_file = "livemcx"
        fieldnames = [
            'Commodity',
            'Price',
            'Chg',
            '%Chg',
            'Open',
            'High',
            'Low',
            'Time',
            'POS',
            'NEG'
        ]
        body = "Commodity, Price, Chg, %Chg, Open, High, Low, Time, POS, NEG\n"
        for datas in scraped_data:
            if datas:
                for data in datas:
                    POS = data['POS']
                    NEG = data['NEG']
                    if (POS >= 1 or NEG <= -1):
                        Commodity = data['Commodity']
                        Price = data['Price']
                        Chg = data['Chg']
                        percentChg = data['%Chg']
                        Open = data['Open']
                        High = data['High']
                        Low = data['Low']
                        Time = data['Time']
                        POS = data['POS']
                        NEG = data['NEG']

                        body += Commodity + \
                                ", " + Price + \
                                ", " + Chg + \
                                ", " + percentChg + \
                                ", " + Open + \
                                ", " + High + \
                                ", " + Low + \
                                ", " + Time + \
                                ", " + str(POS) + \
                                ", " + str(NEG) + "\n"

        print(body)

        # writeCsvFile(name_file, fieldnames, scraped_data)
        # break
        title = "MCX-NCDEX rates"
        notify(title, body)
        time.sleep(60)