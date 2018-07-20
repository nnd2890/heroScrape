

"""
 add the base_url in the @hrefs of document
"""
parser = html.fromstring(response.text)
base_url = "https://www.yellowpages.com"
parser.make_links_absolute(base_url)


"""
 deal with response
"""
try:
    response = requests.get(url, verify=False, headers=headers)
    print("parsing page")
    if response.status_code == 200:

        return results
    elif response.status_code == 404:
        print("Could not find a location matching")
        break
    else:
        print("Failed to process page")
        return []
except:
    print("Failed to process page")
    return []

"""
 get string
"""
def get_string(parser, XPATH):
    arr = parser.xpath(XPATH)
    str = ''.join(arr).strip() if arr else None
    return str

"""
 get number
"""
def get_number(arr):
    if arr:
        str = get_string(arr)
        number = re.findall(r'\d+[,.]?\d+', str)[0].replace(',','')
        return number
    else:
        return None