import urllib.request
from bs4 import BeautifulSoup
import json

def parse_comment_page(page_url):
    user_agent = 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:61.0) Gecko/20100101 Firefox/61.0'
    request = urllib.request.Request(page_url, headers={'User-Agent':user_agent})
    html = urllib.request.urlopen(request).read()
    soup = BeautifulSoup(html, 'html.parser')
    content = soup.find('div', attrs={'class':'qucja8-6'})
    title = content.find('h2', attrs={'class':'s134yi85-0'}).text
    upvotes = content.find('div', attrs={'class':'_1rZYMD_4xY3gRcSS3p8ODO'}).text
    original_poster = content.find('a', attrs={'class':'_2tbHP6ZydRpjI44J3syuqC'}).text
    comments_count = content.find('span', attrs={'class':'FHCV02u6Cp2zYL0fhQPsO'}).text
    comment_area = soup.find('div', attrs={'class':'qucja8-7'})
    comments = comment_area.find_all('div', attrs={'class':'Comment'})
    extracted_comments = []

    for comment in comments:
        commenter = comment.find('a', attrs={'class':'s1461iz-1'}).text
        comment_text = comment.find('div', attrs={'class':'r4x9ih-6'}).text
        extracted_comments.append({'commenter':commenter, 'comment_tex':comment_text})

    post_data = {
        'title':title,
        'upvotes':upvotes,
        'poster':original_poster,
        'no_of_comment':comments_count,
        'comments':extracted_comments
    }
    print(post_data)
    return post_data

url = 'http://www.reddit.com/top'
user_agent = 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:61.0) Gecko/20100101 Firefox/61.0'
request = urllib.request.Request(url, headers={'User-Agent':user_agent})
html = urllib.request.urlopen(request).read()
soup = BeautifulSoup(html, 'html.parser')

main = soup.find('div', attrs={'class':'s1us1wxs-0'})
comment_a_tags = main.find_all('a', attrs={'class':'_1UoeAeSRhOKSNdY_h3iS1O'})
extracted_data = []

for a_tag in comment_a_tags[0:10]:
    url = a_tag['href']
    if not url.startswith('htpp'):
        url = 'http://reddit.com' + url
    print('Extracting data from %s' %url)

    extracted_data.append(parse_comment_page(url))