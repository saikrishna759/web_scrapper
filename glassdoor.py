import requests
import urllib
from bs4 import BeautifulSoup
import html5lib
import time
import lxml
import json
import re
def glassdoor(url,driver):
    proxies = {'http': 'http://user:pass@10.10.1.10:3128/'}
    s = 'not found'
    url = url.replace('https://','')
    url = url.replace('http://','')
    url = url.rstrip('/')
    query = 'glassdoor '+ url + ' overview'
    #print(query)
    query = urllib.parse.quote_plus(query)
    number_result = 20
    google_url = "https://www.google.com/search?q=" + query + "&num=" + str(number_result)
    #response = requests.get(google_url, {"User-Agent": 'sainath'})
    driver.get('http://www.google.com')
    #print("in")
    #print(driver.current_url)
    res = driver.find_element_by_xpath('//*[@id="tsf"]/div[2]/div[1]/div[1]/div/div[2]/input')
    #print("res")

    res.send_keys(query)

    res.send_keys('\n')
    #print(driver.current_url)
    #print("hi")
    soup = BeautifulSoup(driver.page_source, "html.parser")
    #print('gi')
    #print(soup.find('h3',class_ = 'LC20lb DKV0Md').text)
    result_div = soup.find_all('div', attrs={'class': 'yuRUbf'})
    #print(result_div)
    links = []
    titles = []
    descriptions = []
    for r in result_div:
        # Checks if each element is present, else, raise exception
        try:
            link = r.find('a', href=True)
            #print(link['href'])
            #title = r.find('div', attrs={'class': 'vvjwJb'}).get_text()
            #description = r.find('div', attrs={'class': 's3v9rd'}).get_text()

            # Check to make sure everything is present before appending
            if link != '':# and title != '' and description != '':
                #print(link['href'])
                links.append(link['href'])
                # titles.append(title)
                #descriptions.append(description)
        # Next loop if one element is not present
        except:
            continue
    #print(links)
    '''
    to_remove = []
    clean_links = []
    for i, l in enumerate(links):
        clean = re.search('\/url\?q\=(.*)\&sa', l)

        # Anything that doesn't fit the above pattern will be removed
        if clean is None:
            to_remove.append(i)
            continue
        clean_links.append(clean.group(1))
    print(clean_links)
    page = clean_links[0]
    '''
    page = ''
    for j,i in enumerate(links):
        if j >= 3:
            break
        if re.search('www.glassdoor.co.in/Overview',i):
            page = i
            break

    #print(page)
    #page = "https://www.glassdoor.co.in/Reviews/Appinventiv-Reviews-E1032313.htm?sort.sortType=OR&sort.ascending=false&filter.iso3Language=eng"
    response = requests.get(page,proxies = proxies ,headers = {'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/601.3.9 (KHTML, like Gecko) Version/9.0.2 Safari/601.3.9'})
    #print(response.status_code)
    soup = BeautifulSoup(response.text, "html.parser")
    try:
    #print(soup)
    #rate = soup.find('div',class_="v2__EIReviewsRatingsStylesV2__ratingNum v2__EIReviewsRatingsStylesV2__large")
        review = soup.find('div',class_ = 'multipleReviews padTop padHorz')
        rev = {}
        if review is not None:
            #print("review")

            rev['Date'] = review.find('time',class_ = 'date subtle small').text
            #print(rev)
            x = review.find('span',class_ = 'gdStars gdRatings sm margRt')
            rev['rating'] = len(x.find_all('i',class_ = 'star'))
            #print(rev)
            body1 = review.find('p',class_ = 'pros mainText truncateThis wrapToggleStr')
            body2 = review.find('p',class_ = 'cons mainText truncateThis wrapToggleStr')
            rev['body'] = 'pros :'+body1.text+ '|| cons :'+body2.text
            #print(rev)
            rev['name'] = review.find('span',class_ = 'authorJobTitle middle reviewer').text
            #print(rev)
            rev['photo'] = 'null'
            rev['platform'] = 'glassdoor'
            x =  review.find('span',class_ = 'authorLocation')
            if x is not None:
                rev['address'] = x.text
            else:
                rev['address'] = 'null'
            #print(rev)
            #rev['sentiment'] = review.find('span',class_ = 'middle').text

        # print(rev)
        #print(page)
        data = soup.find_all('script', type='application/ld+json')
        data = json.loads(data[0].string)
        maindata = {}
        maindata['overalrating'] = data['ratingValue']
        maindata['ratingcount'] = data['ratingCount']
        maindata['reviews'] = rev
        maindata['url'] = page
    except :
        return {}

    return maindata
