import requests
from lxml.html import fromstring
import random

def get_proxies():
    url = 'https://free-proxy-list.net/'
    response = requests.get(url)
    parser = fromstring(response.text)
    proxies = set()
    for i in parser.xpath('//*[@id="proxylisttable"]/tbody/tr')[:10]:
        if i.xpath('.//td[7][contains(text(), "yes")]'):
            ip = i.xpath('td[1]/text()')[0]
            port = i.xpath('td[2]/text()')[0]
            proxy = ":".join([ip, port])
            proxies.add(proxy)

    proxy = random.sample(proxies, 1)[0]
    proxy = '167.99.157.10:3128'
    proxies = {"http": "http://" + proxy, "https": "http://" + proxy}
    return proxies

proxies = get_proxies()
url = 'https://httpbin.org/ip'
response = requests.get(url, proxies=proxies)
print(response.json())

# url = 'https://httpbin.org/ip'
# for i in range(1,len(proxies)):
#     proxy = next(proxy_pool)
#     print("Request #%d"%i)
#     proxies = {"http": "http://" + proxy, "https": "http://" + proxy}
#     # print(proxies)
#     try:
#         response = requests.get(url, proxies=proxies)
#         print(response.json())
#     except:
#         print("Skipping. Connection error")