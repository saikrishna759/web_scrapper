import requests
import urllib
import re
from bs4 import BeautifulSoup
from datetime import datetime
class playstore:
    def __init__(self,url,driver):
        self.url = url
        self.driver = driver
    def get(self):
        driver = self.driver
        playstoreurl = ''
        url = self.url
        url = url.replace('https://','')
        url = url.replace('http://','')
        url = url.rstrip('/')
        query = 'playstore '+ url+' reviews'
        #print(query)
        query = urllib.parse.quote_plus(query)
        number_result = 20
        google_url = "https://www.google.com/search?q=" + query + "&num=" + str(number_result)
        #proxies = {'http':'http://91.205.174.26:80'}
        #response = requests.get(google_url,headers = {'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/601.3.9 (KHTML, like Gecko) Version/9.0.2 Safari/601.3.9'},proxies=#proxies)
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
        #print(links)
        #print(response)
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
        if len(clean_links)==0:
            return " no links found"
        #print  clean_links)
        '''
        page = links[0]

        #print(clean_links)
        #page += '%26showAllReviews%3Dtrue'
        page = page.replace('%3F','?')
        page = page.replace('%3D','=')
        page = page.replace('%26','&')
        #print(page)
        playstoreurl = page
        resfr = requests.get(page)
        #page += '&showAllReviews=true'
        response = requests.get(page)
        #print(res)
        headers = {'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/601.3.9 (KHTML, like Gecko) Version/9.0.2 Safari/601.3.9'}
        if response.status_code != 200:
            response = requests.get(page,headers = headers)

        #url = 'https://play.google.com/store/apps/details?id=com.skype.raider&hl=en_IN&gl=US'
        #response=requests.get(url)
        rating = 0
        ratingcount = 0
        if response.status_code < 400:
            soup = BeautifulSoup(response.content,'html.parser')
            value = soup.find('div',class_ = 'BHMmbe')
            count = soup.find('span',class_ ='EymY4b')
            perc = soup.find('div',class_ = 'VEF2C')
            perc = str(perc)
            perc = perc.split('width:')
            tot = 0
            star1 = 0
            #print(perc)
            for i in range(1,len(perc)):
                temp = perc[i].strip()
                temp = temp.split("%")
                #print(temp)
                temp = int(temp[0])
                tot = tot+temp
                star1 = temp
            try :
                rating = value.text
                tempc = count.text
                #print(value,count)
                tempc = tempc.split(' ')
                tempc = tempc[0]
                ratingcount = tempc
            except:
                pass
        star1ratio = 0
        if tot>0:
            star1ratio = star1/tot
        #print(rating,ratingcount,star1ratio)
        ar = response.text.split('https://play-lh.googleusercontent.com/Yq7')
        rev = []
        for i in ar[1:]:
            i = str(i)
            t = str(i)
            #i=i.replace("[","]")
            ar = t.split('gp:')
            tmpr = ['','']
            if len(ar) > 1:
                tmp = ar[1].replace('[','')
                tmp = tmp.replace(']','')
                tmpr =  tmp.split(',')
            tmp = i.split(']')
            for j in tmp:
                if len(j) > 350:
                    var = j.split('[')
                    ts = var[1].split(',')
                    try:ts = int(ts[0])
                    except:continue
                    rev.append([var[0],tmpr[1],tmpr[7],ts])

        revar = []
        for i in range(len(rev)):
            tmp = rev[i][0]
            try :
                #print(tmp[2])
                tmprat = int(tmp[2])
                #print(tmp)
                tmprev = tmp[10:-2]
                date = datetime.fromtimestamp(rev[i][3])
                #print(date)
                date = str(date)
                date = date.split(' ')
                #print(date)
                date = date[0]
                #print(date)
                date = date.split('-')
                #print(date)
                months = ['','January','February','March','April','May','June','July','August','September','October','November','December']
                time = str(date[2])+' '
                time += months[int(date[1])]+','+date[0]
                #print(time)
                revar.append([tmprat,tmprev,rev[i][1],rev[i][2],time])
            except:
                s = ''
        d = {}
        return[rating,ratingcount,revar,star1ratio,playstoreurl]
