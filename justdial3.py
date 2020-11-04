import requests
import urllib
from bs4 import BeautifulSoup
import html5lib
import lxml
import json
import re
#from selenium import webdriver
#from selenium.webdriver.chrome.options import Options
import time
'''
options = Options()
options.add_argument("--headless")
options.add_argument("--disable-notifications")
options.add_argument("--lang=en-GB")
driver = webdriver.Chrome("C:\\Users\\saikrishna\\Desktop\\sai\\magicpins\\chromedriver85.exe",chrome_options=options)
'''
def justdial(url,driver):
    proxies = {'http': 'http://user:pass@10.10.1.10:3128/'}
    s = 'not found'
    url = url.split('.')[1]
    #print(url)
    #url = url.replace('https://www.','')
    #url = url.replace('http://www.','')
    #url = url.replace('.com','')
    #url = url.rstrip('/')

    query = 'justdial '+str(url)

    driver.get('http://www.google.com')

    res = driver.find_element_by_xpath('//*[@id="tsf"]/div[2]/div[1]/div[1]/div/div[2]/input')

    res.send_keys(query)

    res.send_keys('\n')

    #print("hi")
    time.sleep(2)
    #print(driver.current_url)
    soup = BeautifulSoup(driver.page_source,"html.parser")
    result_div = soup.find_all('div', attrs={'class': 'g'})

    links = []
    titles = []
    descriptions = []
    #for r in result_div:
    #rats = []
    while True:
        r = result_div[0]
        try:
            link0 = r.find('div',class_ = 'yuRUbf')
            link = link0.find('a', href=True)
            #print(link)
            des = r.find('div', attrs={'class': 'IsZvec'})
            dec = des.find('div')
            dec = dec.find('span',class_ = 'aCOpRe')
            description  = dec.find('span').text
            #print(description)
            try:
                rat = des.find('div',class_ = 'fG8Fp uo4vr')
                rat = rat.find_all('span')
                rat = rat[2].text + ' '+ rat[3].text
            except:
                rat = None
            #print("r",rat)
            #description  = des.find('span',class_ = 'aCOpRe')


            #description  = description.find('span').text
            #prit(description)

        except:
            #print("exception")
            continue
        break

    page = link['href']
    #print("res",page)
    decription = description
    ans = ''
    rat = rat
    #print("rat",rat)
    #print("des",description)
    rating = 0
    count = 0

    h = page.split('/')

    for c in h:

        if len(c.split('-')) > 1:
            c =  c.replace('-','')
        if re.search('^'+str(url).lower(),c.lower()):
            f = True

            ans = ''
            break
        else:
            f = False
            ans = 'not found'

    if f:
        if rat is not None:

            ans = rat

            t = ans.split(' ')

            t[3] = t[3].replace('(','')
            t[3] = t[3].replace(')','')
            rating = float(t[1])
            count = int(t[2])

        else:
            if re.search('rated.*based on.*r',description.lower()):
                p = re.compile('rated.*based on.*r')
                ans = p.findall(description.lower())
                t = ans[0].split(' ')
                rating = float(t[1])
                count = int(t[4])
                #ans = description
            else:
                page = None
                f = False
                ans = 'not found'

    else:
        page = None


    final = {'rating':rating,'count':count,'url':page}
    return final

#print(justdial("http://www.migrocer.com",driver))
