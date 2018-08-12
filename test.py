import requests
from lxml import html
import unicodecsv as csv
from multiprocessing import Pool as ThreadPool
import re
import sys, os
import json
import time
from mysql_database import MysqlDatabase

def parse_listing(url):
    headers = {
               'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36'
               }

    proxy = '43.249.143.89:31191'
    proxies = {"http": "http://" + proxy, "https": "http://" + proxy}
    scraped_results = []
    try:
        response = requests.get(url, verify=False, headers = headers)
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
                    'perChg':percentChg,
                    'Open':Open,
                    'High':High,
                    'Low':Low,
                    'Time':Time,
                    'POS':POS,
                    'NEG':NEG
                }

                if (POS >= 1 or NEG <= -1):
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

def writeCsvFile(name_file, fieldnames, scraped_data):
    with open('%s.csv' % name_file, 'wb') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames, quoting=csv.QUOTE_ALL)
        writer.writeheader()
        for datas in scraped_data:
            if datas:
                for data in datas:
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

    live_database = MysqlDatabase()

    while True:
        pool = ThreadPool(10)
        scraped_data = pool.map(parse_listing, url_list)
        pool.terminate()
        pool.join()

        name_file = "livemcx"
        fieldnames = [
            'Commodity',
            'Price',
            'Chg',
            'perChg',
            'Open',
            'High',
            'Low',
            'Time',
            'POS',
            'NEG'
        ]
        # body = "Commodity, Price, Chg, %Chg, Open, High, Low, Time, POS, NEG\n"
        body = ""
        for datas in scraped_data:
            if datas:
                for data in datas:
                    if data:
                        Commodity = data['Commodity']
                        Price = data['Price']
                        Chg = data['Chg']
                        percentChg = data['perChg']
                        Open = data['Open']
                        High = data['High']
                        Low = data['Low']
                        Time = data['Time']
                        POS = data['POS']
                        NEG = data['NEG']

                        # body += Commodity + \
                        #         ", " + Price + \
                        #         ", " + Chg + \
                        #         ", " + percentChg + \
                        #         ", " + Open + \
                        #         ", " + High + \
                        #         ", " + Low + \
                        #         ", " + Time + \
                        #         ", " + str(POS) + \
                        #         ", " + str(NEG) + "\n"

                        table = "live"
                        col = "Commodity"

                        # check record is existed on database
                        if live_database.row_existed(table, col, Commodity):
                            record = live_database.select_field_where(table, col, Commodity)
                            record_len = len(record)
                            record_POS = record[record_len-2]
                            record_NEG = record[record_len-1]
                            record_id = record[0]

                            if (record_POS != POS) or (record_NEG != NEG):
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
                                live_database.update_row(table, data, record_id)
                        else:
                            live_database.insertRow(table, data)
        if body:
            body = "Commodity, Price, Chg, %Chg, Open, High, Low, Time, POS, NEG\n" + body
            print(body)
            # writeCsvFile(name_file, fieldnames, scraped_data)
            title = "MCX-NCDEX rates"
            notify(title, body)
        else:
            print("dont get new content")
        time.sleep(60)

