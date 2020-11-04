import requests
import time
import urllib
import re
from bs4 import BeautifulSoup
from datetime import datetime
from facebook2 import fb
class facebook:
    def __init__(self,url,driver):
        self.url = url
        self.driver = driver
    def get(self):
        driver = self.driver
        d = {}
        url = self.url
        url = url.replace('https://','')
        url = url.replace('http://','')
        url = url.rstrip('/')
        query = 'facebook '+ url
        ##print(query)
        query = urllib.parse.quote_plus(query)
        number_result = 20
        google_url = "https://www.google.com/search?q=" + query + "&num=" + str(number_result)
        #fb(google_url)
        headers = {'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/601.3.9 (KHTML, like Gecko) Version/9.0.2 Safari/601.3.9'}
        #response = requests.get(google_url,headers=headers)
        #print(
        #if response.status_code == 429:
            #print("429 occ")
            #time.sleep(int(response.headers["Retry-After"]))
        driver.get('http://www.google.com')
        # print("in")
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
        '''
        soup = BeautifulSoup(response.text, "html.parser")
        result_div = soup.find_all('div', attrs={'class': 'ZINbbc'})
        links = []
        titles = []
        descriptions = []
        for r in result_div:
            # Checks if each element is present, else, raise exception
            try:
                link = r.find('a', href=True)
                title = r.find('div', attrs={'class': 'vvjwJb'}).get_text()
                description = r.find('div', attrs={'class': 's3v9rd'}).get_text()

                # Check to make sure everything is present before appending
                if link != '' and title != '' and description != '':
                    links.append(link['href'])
                    titles.append(title)
                    descriptions.append(description)
            # Next loop if one element is not present
            except:
                continue

        to_remove = []
        clean_links = []
        for i, l in enumerate(links):
            clean = re.search('\/url\?q\=(.*)\&sa', l)

            # Anything that doesn't fit the above pattern will be removed
            if clean is None:
                to_remove.append(i)
                continue
            clean_links.append(clean.group(1))
        '''
        #print(links)
        fblinks = []
        for i in links:
            if len(i.split('facebook'))>1:
                fblinks.append(i)
        fburl = ''
        for i in fblinks:
            cname = url.split('.')
            cname = cname[1]
            if re.search(cname,i,re.IGNORECASE) is not None:
                fburl = i
                break
        ans = ''
        c = 0
        for i in range(len(fburl)):
            if c < 4:
                ans += fburl[i]
                if fburl[i] == '/':
                    c += 1
        fburl = ans
        #fburl.strip('/')
        d['fburl'] = str(fburl)
        fburl = fburl.replace('www','en-gb')

        if fburl[-1] != '/':fburl += '/reviews'
        else:fburl+='reviews'
        searchurl = fburl
        #searchurl += '?locale2=en_GS'
        #d['fburl'] = searchurl
        if searchurl != '':
            #print(searchurl)
            #res = fb(searchurl)
            try:
                driver.get(searchurl)
            except:
                pass
            time.sleep(2)
            #print(self.driver.current_url)
            #print("ok")
            SCROLL_PAUSE_TIME = 2
            last_height = self.driver.execute_script("return document.body.scrollHeight")
            i = 0

            while True:
                if i >= 2:
                    break
                i += 1
                try:self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                except:pass
                time.sleep(SCROLL_PAUSE_TIME)


                try:new_height = self.driver.execute_script("return document.body.scrollHeight")
                except:pass
                if new_height == last_height:
                    break
                last_height = new_height
            #print(driver.current_url)
        #wait = WebDriverWait(self.driver, 10)
        #element = wait.until(EC.presence_of_element_located(((By.CLASS_NAME, newclass))))
        #print(elemen
            try:
                if True:
                    soup = BeautifulSoup(driver.page_source,'html.parser')
                #print(soup)
                    rat = soup.find_all('div',class_ = '_672g _1f47')
                    for i in rat:
                        try:
                            k = float(i.text)
                            rat = k
                            break
                        except:
                            s = ''
                    d['rating'] = rat
                    reviews = soup.find_all('div',class_ = '_1dwg _1w_m _q7o')
                    rev = None
                    count = soup.find('span',class_='_67l2')
                    count = count.text
                    count = count.split(' ')
                    count = int(count[5])
                    d['count'] = count
                    #print(reviews)
                    d['review'] = []
                    for i in reviews:
                        #tmp = i[1].split('More options')
                        review = {}
                        date = i.find('span',class_='timestampContent')
                        review['Date'] = date.text
                        body = i.find('div',class_ = '_5pbx userContent _3576')
                        #review['body'] = tmp[1].replace('comment','')
                        review['body'] = body.text
                        rev = i.text
                        #review = {}
                        i = rev.split('.')
                        if len(i[0].split('doesn\'t'))>1:
                            tmp = i[0].split('doesn\'t')
                            review['name'] = tmp[0].strip()
                            review['sentiment'] = 'Negative'
                            review['rating'] = 1
                        else:
                            tmp = i[0].split('recommend')
                            review['name'] = tmp[0].strip()
                            review['sentiment'] = 'Positive'
                            review['rating'] = 5
                        #tmp = i[1].split('More options')
                        d['review'].append(review)
            except:
                pass
        #print('from facebook')
        #print(d)
        return d

