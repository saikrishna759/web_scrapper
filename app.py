from flask import Flask,jsonify,request
import requests
from facebook import facebook
from justdial3 import justdial
from playstore import playstore
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import html5lib
import lxml
import re
import json
from glassdoor import glassdoor
import urllib.request
from googleplace2 import googlemap1

def drive():
    #print("drive")
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--disable-notifications")
    options.add_argument("--lang=en-GB")
    input_driver = webdriver.Chrome(options=options)
    return input_driver

def fbreviews(latestpositivereview,latestnegativereview,data,lpr,lnr,trs):
    #print(data,latestpositivereview)
    try:
        if len(lpr)<5:
            if data['rating']>2:
                #print('lpr')
                latestpositivereview['body']=data['body']
                latestpositivereview['author_name']= data['name']
                latestpositivereview['platform'] = 'Facebook'
                #latestpositivereview['business_address'] = data['address']
                latestpositivereview['reviewed_at'] = data['Date']
                latestpositivereview['rating']=data['rating']
                if data['rating'] == 3:
                    latestpositivereview['sentiment'] = 'Neutral'
                else:
                    latestpositivereview['sentiment'] = 'Positive'
                lpr.append(dict(latestpositivereview))
                latestpositivereview = dict(trs)
        if len(lnr)<5:
            if data['rating']<3:
                latestnegativereview['body']=data['body']
                latestnegativereview['author_name']= data['name']
                latestnegativereview['platform'] = 'Facebook'
                #latestnegativereview['business_address'] = data['address']
                latestnegativereview['reviewed_at'] = data['Date']
                latestnegativereview['sentiment'] = 'Negative'
                latestnegativereview['rating'] = data['rating']
                lnr.append(dict(latestnegativereview))
                latestnegativereview = dict(trs)
    except:
        return

def gdreviews(latestpositivereview,latestnegativereview,data,lpr,lnr,trs):
    #print(data,latestpositivereview)
    try:
        if len(lpr)<5:
            if data['rating']>2:
                #print('lpr')
                latestpositivereview['body']=data['body']
                latestpositivereview['author_name']= data['name']
                latestpositivereview['platform'] = 'Glassdoor'
                latestpositivereview['business_address'] = data['address']
                latestpositivereview['reviewed_at'] = data['Date']
                latestpositivereview['rating']=data['rating']
                if data['rating'] == 3:
                    latestpositivereview['sentiment'] = 'Neutral'
                else:
                    latestpositivereview['sentiment'] = 'Positive'
                lpr.append(dict(latestpositivereview))
                latestpositivereview = dict(trs)
        if len(lnr)<5:
            if data['rating']<3:
                latestnegativereview['body']=data['body']
                latestnegativereview['author_name']= data['name']
                latestnegativereview['platform'] = 'Glassdoor'
                latestnegativereview['business_address'] = data['address']
                latestnegativereview['reviewed_at'] = data['Date']
                latestnegativereview['sentiment'] = 'Negative'
                latestnegativereview['rating'] = data['rating']
                lnr.append(dict(latestnegativereview))
                latestnegativereview = dict(trs)
    except:
        return
def googlereviews(latestpositivereview,latestnegativereview,data,lpr,lnr,trs):
    try:
        #print("came")
        if len(lpr)<5:
            if data['rating']>2:
                latestpositivereview['body']=data['body']
                latestpositivereview['author_name']= data['name']
                latestpositivereview['platform'] = 'Google'
                latestpositivereview['business_address'] = data['address']
                latestpositivereview['reviewed_at'] = data['Date']
                latestpositivereview['rating'] = data['rating']
                if data['rating'] == 3:
                    latestpositivereview['sentiment'] = 'Neutral'
                else:
                    latestpositivereview['sentiment'] = 'Positive'
                lpr.append(dict(latestpositivereview))
                latestpositivereview = dict(trs)
        if len(lnr)<5:
            if data['rating']<3:
                latestnegativereview['body']=data['body']
                latestnegativereview['author_name']= data['name']
                latestnegativereview['platform'] = 'Google'
                latestnegativereview['business_address'] = data['address']
                latestnegativereview['reviewed_at'] = data['Date']
                latestnegativereview['sentiment'] = 'Negative'
                latestnegativereview['rating'] = data['rating']
                lnr.append(dict(latestnegativereview))
                latestnegativereview = dict(trs)
        #print("out cm")
    except:
        #print("except grev")
        return
app = Flask(__name__)

@app.route("/",methods=["POST", "GET"])
def index():
    #return googlemap1()
    driver = drive()
    averagerating = 0
    facebookurl = None
    googlebusinessurl = None
    null = None
    detectedurls = []
    lpr =[]
    lnr = []
    latestpositivereview = {'rating':null,'body':null,'author_name':null,'author_photo':null,'page_name':null,'page_photo':null,'platform':null,'reviewed_at':null,'business_address':null,'sentiment':null}
    latestnegativereview = {'rating':null,'body':null,'author_name':null,'author_photo':null,'page_name':null,'page_photo':null,'platform':null,'reviewed_at':null,'business_address':null,'sentiment':null}
    temp_review_structure = {'rating':null,'body':null,'author_name':null,'author_photo':null,'page_name':null,'page_photo':null,'platform':null,'reviewed_at':null,'business_address':null,'sentiment':null}
    totalreviews = 0
    psrating = 0
    star1reviews = 0
    psratingcount = 0
    errormessage = ''
    #print(p.get())
    #tryselenium()
    flag = False
    #print(request.args)
    temps = ''
    for i in request.args:
        if i == 'url':
            temps += request.args[i]
        else:
            temps += '&'
            temps += i
    input1 = temps
    #input1 = request.args['url']
    #print(input1)
    #input1 = 'https://'+input1
    headers = {'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/601.3.9 (KHTML, like Gecko) Version/9.0.2 Safari/601.3.9'}
    try:
        if re.search('https://',input1) or re.search('http://',input1):

            response = requests.get(input1,headers = headers)
            #print("request")
            if response.status_code == 404:
                #print("status eror")
                return jsonify({"status":"false","error_message":"invalid company url"})
        else:
            flag = True
        greviews = ''
        try :
            greviews = googlemap1(input1,driver)
            #print(greviews)
        except:
            pass
        if len(greviews) != 0:
            try:
                #print(" page")
                stars1 = greviews['1starrating']
                stars1 = stars1.split(' ')
                stars1 = int(stars1[2])
                star1reviews += stars1
            except:
                pass
            try:
                grev= greviews['reviews']
                for i in grev:
                    i['address'] = None
                    latestnegativereview = dict(temp_review_structure)
                    latestpositivereview = dict(temp_review_structure)
                    #print("add0")
                    googlereviews(latestpositivereview,latestnegativereview,i,lpr,lnr,temp_review_structure)
                    #print("Add1")
            except:
                pass
            try:
                detectedurls.append({'name':'Google','url':greviews['company_url']})
                googlebusinessurl = greviews['company_url']
            except:
                pass
            try:
                rat = float(greviews['overalrating'])
                ratc = greviews['ratingcount']
                #ratc = ratc.replace(')','')
                ratc = ratc.split(' ')
                #print(ratc)
                ratc = ratc[0].replace(',','')
                #print(ratc)
                ratc = int(ratc)
                averagerating += rat*ratc
                totalreviews += ratc
                #print("final")
            except Exception as e:
                pass
                #print(str(e))
        try:
            if flag:
                pageurl = greviews['pagesite']
                if  pageurl != '':
                    input1 = pageurl
                else:
                    input1 = input1.split(',')[0]
            #print(input1)
        except:
            pass
        #print("ps0")
        psreview =  playstore(input1,driver).get()
        #print("ps")
        try :
            tmp= psreview[0].split('.')
            psrating += int(tmp[0])
            if len(tmp)> 1:
                val = int(tmp[1])
                psrating += (val/10)
            #print(psrating)
            tmp = psreview[1].split(' ')
            #print(tmp)
            tmp = tmp[0].replace(",","")
            #print(tmp)
            psratingcount = int(str(tmp))
        except:
            psrating = 0
            psratingcount = 0

        averagerating += psrating*psratingcount
        totalreviews += psratingcount
        try:
            star1reviews += int(psratingcount*psreview[3])
        except:
            s = ''
        for i in psreview[2]:
            #print(i)
            try :
                rat1 = int(i[0])
                if rat1 > 2 and len(lpr)<5:
                    maxr = rat1
                    latestpositivereview['rating']=rat1
                    latestpositivereview['body']= i[1]
                    latestpositivereview['author_name'] = i[2]
                    latestpositivereview['author_photo'] = i[3]
                    latestpositivereview['platform'] = 'Playstore'
                    latestpositivereview['page_name'] = i[2]
                    latestpositivereview['page_photo'] = i[3]
                    latestpositivereview['reviewed_at'] = i[4]
                    if rat1 > 3:
                        latestpositivereview['sentiment'] = 'positive'
                    elif rat1 < 3:
                        latestpositivereview['sentiment'] = 'Negative'
                    else:
                        latestpositivereview['sentiment'] = 'Neutral'
                    lpr.append(dict(latestpositivereview))
                    latestpositivereview = dict(temp_review_stucture)
                elif rat1 < 3 and len(lnr)<5:
                    minr = rat1
                    latestnegativereview['rating'] = rat1
                    latestnegativereview['body']= i[1]
                    latestnegativereview['author_name']= i[2]
                    latestnegativereview['author_photo']=i[3]
                    latestnegativereview['platform'] = 'Playstore'
                    latestnegativereview['page_name']=i[2]
                    latestnegativereview['page_photo'] = i[3]
                    latestnegativereview['reviewed_at'] = i[4]
                    if rat1>3:
                        latestnegativereview['sentiment'] =  'Positive'
                    elif rat1<3:
                        latestnegativereview['sentiment'] = 'Negative'
                    else:
                        latestnegativereview['sentiment'] = 'Neutral'
                    lnr.append(dict(latestnegativereview))
                    latestnegativereview = dict(temp_review_structure)
            except :
                #psreview = None
                s =''
        try:
            match_str = 'https://play.google.com/'
            if re.match(match_str,psreview[4]):
                detectedurls.append({'name':'Playstore','url':psreview[4]})
        except:pass
        #:print('gd')
        try:
            gdoor = glassdoor(input1,driver)
        except:
            #gdoor = None
            pass
        #print('gd')
        try:
            rat = gdoor['overalrating'].split('.')
            scr = int(rat[0])+int(rat[1])/10
            rat = scr
            ratc = int(gdoor['ratingcount'])
            averagerating += rat*ratc
            totalreviews += ratc
        except:
            gdoor = None
            pass
        try:
            latestnegativereview = dict(temp_review_structure)
            latestpositivereview = dict(temp_review_structure)
            gdreviews(latestpositivereview,latestnegativereview,gdoor['reviews'],lpr,lnr,temp_review_structure)
        except:
            pass
        try:
            temp_url = gdoor['url']
            match_string = 'https://www.glassdoor.co.in/'
            if re.match(match_string,temp_url)!= None:
                detectedurls.append({'name':'Glassdoor','url':gdoor['url']})
        except:pass
        #return glassdoor(input1)
        try:
            fb = facebook(input1,driver)
            fbrev = fb.get()
            try:
                facebookurl = fbrev['fburl']
                detectedurls.append({'name':'Facebook','url':fbrev['fburl']})
            except:
                pass
            try:
                for i in fbrev['review']:
                    latestnegativereview = dict(temp_review_structure)
                    latestpositivereview = dict(temp_review_structure)
                    fbreviews(latestpositivereview,latestnegativereview,i,lpr,lnr,temp_review_structure)
            except:
                pass
            try:
                averagerating += fbrev['rating']*fbrev['count']
                totalreviews += fbrev['count']
            except:
                pass
        except Exception as e:
            s = ''
            #print(str(e))
        try:
            jdreviews = justdial(input1,driver)
            #print(jdreviews)
            averagerating += jdreviews['rating']*jdreviews['count']
            totalreviews += jdreviews['count']
            if re.match('https://www.justdial.com/',jdreviews['url']) != None:
                detectedurls.append({'name':'Justdial','url':jdreviews['url']})
        except:
            s = ''
        '''
        try:
            z = zomato(input1)
            zurl = z.get()
            turl = zurl['url']
            if len(turl.split('/'))>4:
                detectedurls.append({'name':'Zomato','url':turl})
        except Exception as e:
            #print(str(e))
            pass
        '''
        #print("enf0")
        businessname = input1.replace('http://','')
        businessname = businessname.replace('https://','')
        businessname = businessname.replace('/','')
        if totalreviews>0:
            averagerating = int((averagerating/totalreviews)*10)
        averagerating = averagerating/10
        #print("end1")
        try:
            return jsonify({
                          "status": "true",
                                    "data": {
                                    "business_name": businessname,
                                    "overall_rating": averagerating,
                                    "total_reviews": totalreviews,
                                    "unanswered_reviews":'null',
                                    "one_star_review": star1reviews,
                                    "detected_business": detectedurls,
                                    "review_sentiment": {
                                        "positive": 'null',
                                        "negative": 'null',
                                        "neutral": 'null'
                                        },
                                    "latest_positive_review":lpr,
                                    "latest_negative_review":lnr
                                    }
                        })
            #print("completed")
        except:
            #print("final error")
            return jsonify({"status":"false","error_message":'Some error occured look into description : '+str(e)})


    except Exception as e:
        return jsonify({"status":"false","error_message":'Some error occured look into description : '+str(e)})

if __name__ == "__main__":
    app.run(host = '0.0.0.0',port = 8080)
