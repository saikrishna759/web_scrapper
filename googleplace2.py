from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from datetime import datetime,timedelta
import time
import re
#import logging
import traceback

GM_WEBPAGE = 'https://www.google.com/maps/'
MAX_WAIT = 5
MAX_RETRY = 2
MAX_SCROLLS = 3
final_address= ''
final_review_count = ''
company_url = ''
googlemapdata = {}
class GoogleMapsScraper:

    def __init__(self,driver,debug=False):
        self.debug = debug
        self.driver = driver
        #self.logger = self.__get_logger()

    def __enter__(self):
        return self
    def __exit__(self, exc_type, exc_value, tb):
        if exc_type is not None:
            traceback.print_exception(exc_type, exc_value, tb)

        #self.driver.close()
        #self.driver.quit()

        return True

    def get_reviews(self, offset):

        self.__scroll()
        #self.__expand_reviews()
        #print("in")
        time.sleep(3)
        response = BeautifulSoup(self.driver.page_source, 'html.parser')
        googlemapdata['ratingcount'] = response.find('div',class_ = "gm2-caption").text
        googlemapdata['overalrating'] = response.find('div',class_ = "gm2-display-2").text
        googlemapdata['1starrating'] = response.find_all('tr',class_ ="jqnFjrOWMVU__histogram")[4]["aria-label"]
        rblock = response.find_all('div', class_='section-review-content')
        parsed_reviews = []
        for index, review in enumerate(rblock):
            if index >= offset:
                parsed_reviews.append(self.__parse(review))
        #print("out")
        return parsed_reviews
    def sort_by_date(self, oldurl):
        global final_address
        global final_review_count
        global company_url
        self.driver.get(GM_WEBPAGE)


        #print("done")
        time.sleep(2)

        res = self.driver.find_element_by_xpath('//*[@id="searchboxinput"]')
        res.send_keys(oldurl)
        self.driver.find_element_by_xpath('//*[@id="searchbox-searchbutton"]').click()
        wait = WebDriverWait(self.driver, MAX_WAIT)
        #print("hi")
        clicked = False
        tries = 0
        while not clicked and tries < MAX_RETRY:
            try:

                #print("try")
                menu_bt = wait.until(EC.element_to_be_clickable((By.XPATH, '//button[@data-value=\'Sort\']')))
                menu_bt.click()

                clicked = True

            except Exception as e:
                tries += 1

            if tries == MAX_RETRY:
                return -1
        pagesite = ''
        try:
            webaddress = self.driver.find_element_by_xpath('//*[@id="pane"]/div/div[1]/div/div/div[10]/button/div[1]/div[2]/div[1]')
            if '.' in str(webaddress.text):
                pagesite = str(webaddress.text)
                #print(pagesite)

        except Exception as e:
            pass
        # second element of the list: most recent
        recent_rating_bt = wait.until(EC.element_to_be_clickable((By.XPATH, '//li[@role=\'menuitemradio\']')))

        recent_rating_bt = self.driver.find_elements_by_xpath('//li[@role=\'menuitemradio\']')[2]
        recent_rating_bt.click()
        time.sleep(3)
        url = self.driver.current_url
        company_url =url
        googlemapdata['company_url'] = company_url
        #print(company_url)
        googlemapdata['pagesite'] = pagesite

        # wait to load review (ajax call)


        return 0

    def positive(self):

        wait = WebDriverWait(self.driver, MAX_WAIT)

        menu_bt = wait.until(EC.element_to_be_clickable((By.XPATH, '//button[@data-value=\'Sort\']')))
        menu_bt.click()

        recent_rating_bt = wait.until(EC.element_to_be_clickable((By.XPATH, '//li[@role=\'menuitemradio\']')))

        recent_rating_bt = self.driver.find_elements_by_xpath('//li[@role=\'menuitemradio\']')[3]
        recent_rating_bt.click()
        #print("sort 2")
        # wait to load review (ajax call)
        time.sleep(3)

        return 0


    def __parse(self, review):

        item = {}

        id_review = review.find('button', class_='section-review-action-menu')['data-review-id']
        username = review.find('div', class_='section-review-title').find('span').text

        try:
            review_text = self.__filter_string(review.find('span', class_='section-review-text').text)
        except Exception as e:
            review_text = None

        rating = float(review.find('span', class_='section-review-stars')['aria-label'].split(' ')[1])
        relative_date = review.find('span', class_='section-review-publish-date').text

        try:
            review
            n_reviews_photos = review.find('div', class_='section-review-subtitle').find_all('span')[1].text
            metadata = n_reviews_photos.split('\xe3\x83\xbb')
            if len(metadata) == 3:
                n_photos = int(metadata[2].split(' ')[0].replace('.', ''))
            else:
                n_photos = 0

            idx = len(metadata)
            n_reviews = int(metadata[idx - 1].split(' ')[0].replace('.', ''))

        except Exception as e:
            n_reviews = 0
            n_photos = 0

        user_url = review.find('a')['href']
        item['address'] = 'N'
        item['id_review'] = id_review
        item['body'] = review_text
        item['Date'] = relative_date
        item['rating'] = rating
        item['name'] = username
        item['n_review_user'] = n_reviews
        item['n_photo_user'] = n_photos
        item['url_user'] = user_url

        return item

    def __expand_reviews(self):
        # use XPath to load complete reviews
        links = self.driver.find_elements_by_xpath('//button[@class=\'section-expand-review blue-link\']')
        for l in links:
            l.click()
        #time.sleep()


    def __scroll(self):
        scrollable_div = self.driver.find_element_by_css_selector('div.section-layout.section-scrollbox.scrollable-y.scrollable-show')
        self.driver.execute_script('arguments[0].scrollTop = arguments[0].scrollHeight', scrollable_div)

    def __get_driver(self, debug=False):
        options = Options()

        if not self.debug:
            pass#options.add_argument("--headless")

        else:
            options.add_argument("--window-size=1366,768")

        options.add_argument("--disable-notifications")
        options.add_argument("--lang=en-GB")
        input_driver = webdriver.Chrome("C:\\Users\\saikrishna\\Desktop\\sai\\magicpins\\chromedriver85.exe",chrome_options=options)

        return input_driver

    def __filter_string(self, str):
        strOut = str.replace('\r', ' ').replace('\n', ' ').replace('\t', ' ')
        return strOut

def googlemap1(url,driver):
    N = 5
    url = url.replace('https://www.','')
    url = url.replace('http://','')
    url = url.rstrip('/')
    #print(url)
    with GoogleMapsScraper(driver,debug=False) as scraper:
        reviews1 = []
        try:
            error = scraper.sort_by_date(url)
            #print(error)
            if error == 0:
                n = 0
                while n < N:
                    reviews = scraper.get_reviews(n)
                    if len(reviews) == 0:
                        break
                    for r in reviews:
                        reviews1.append(r)
                    n += len(reviews)
                    break

                #print("##########################")

            else:
                #print("no page")
                return {}
            error = scraper.positive()
            if error == 0:
                n = 0
                while n < N:
                    reviews = scraper.get_reviews(n)
                    if len(reviews) == 0:
                        break
                    for r in reviews:
                        reviews1.append(r)
                    n += len(reviews)
                    break
        except:
            pass
        googlemapdata['reviews'] = reviews1
        return googlemapdata


#print(googlemap1('http://appinventiv.com/'))
