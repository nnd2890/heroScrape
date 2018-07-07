import urllib.request
from bs4 import BeautifulSoup
import json

url = 'http://www.reddit.com/top'
request = urllib.request.Request(url)
html = urllib.request.urlopen(request).read()

soup = BeautifulSoup(html, 'html.parser')
main = soup.find('div', attrs={'class':'s1us1wxs-0'})
links = main.find_all('a', attrs={'class':'SQnoC3ObvgnGjWt90zD9Z'})

extracted_records = []
for link in links:
    title = link.text
    url = link['href']
    if not url.startswith('http'):
        url = 'http://reddit.com' + url
    record = {
        'title':title,
        'url':url
    }
    extracted_records.append(record)

with open('data.json', 'w') as outfile:
    json.dump(extracted_records, outfile)