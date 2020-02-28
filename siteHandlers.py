'''
Functions for crawling discount data
'''

import requests 
from bs4 import BeautifulSoup
from abc import ABC, abstractmethod 

class SiteHandlerException(Exception):
    pass

class SiteHandler(ABC):
    HEADERS = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) '\
                      'AppleWebKit/537.36 (KHTML, like Gecko) '\
                      'Chrome/51.0.2704.79 Safari/537.36'}

    def __init__(self, functionName, siteUrl):
        self.functionName = functionName
        self.siteUrl = siteUrl
        self.urls = []
    
    @abstractmethod
    def addUrls(self):
        pass
    
    def returnUrls(self, resultDict):
        self.addUrls()
        resultDict[self.functionName] = self.urls
        if not self.urls:
            resultDict[self.functionName] = SiteHandlerException(self.functionName)  
     
class PageSiteHandler(SiteHandler):
    def __init__(self, functionName, 
                 siteUrl,
                 pageHandler):
        super().__init__(functionName, siteUrl)
        self.pageHandler = pageHandler
        
    def addUrls(self):
        try:
            r = requests.get(self.siteUrl, headers=self.HEADERS)
            self.urls = self.pageHandler(
                BeautifulSoup(r.text,'html.parser'))
        except Exception as e: 
            #raise e
            pass
  
class MultiPageSiteHandler(SiteHandler):
    def __init__(self, functionName, 
                 siteUrl, mainHandlerFunc, 
                 couponHandlerFunc):
        super().__init__(functionName, siteUrl)
        self.mainHandlerFunc = mainHandlerFunc
        self.couponHandlerFunc = couponHandlerFunc
    
    def addUrls(self):
        try:
            r = requests.get(self.siteUrl, headers=self.HEADERS)
            urlsCoupon = self.mainHandlerFunc(
                BeautifulSoup(r.text,'html.parser'))
            for url in urlsCoupon:
                r = requests.get(url, headers=self.HEADERS)
                self.urls.append(self.couponHandlerFunc(
                    BeautifulSoup(r.text,'html.parser')))
        except Exception as e: 
            #raise e
            pass

# single page classes 
class KeeperCouponHandler(PageSiteHandler):
    def __init__(self):
        functionName = 'KeeperCouponHandler'
        siteUrl = 'https://keepercoupon.com/'
        def handler(soup):
            return [
            a.get('href') for a in \
            soup.findAll(
                'a', 
                {'class': 'coupon-code-link button promotion'})]
        
        super().__init__(functionName, siteUrl, handler) 

class DiscountsGlobalHandler(PageSiteHandler):
    def __init__(self):
        functionName = 'DiscountsGlobalHandler'
        siteUrl = 'http://udemycoupon.discountsglobal.com/coupon-category/free-2/'
        def handler(soup):
            return [
                div.find(
                        'div', 
                        {'class': 'link-holder'}).find('a').get('href')\
                    for div in \
                        soup.findAll('div', {'class': 'item-panel'})]
        
        super().__init__(functionName, siteUrl, handler)        

class Guru99Handler(PageSiteHandler):
    def __init__(self):
        functionName = 'Guru99Handler'
        siteUrl = 'https://www.guru99.com/free-udemy-course.html'
        def handler(soup):
            urls = []
            for i, row in enumerate(soup.find('table').findAll('tr')):
                if i==0: continue 
                a = row.findAll('td')[1].find('a')
                urls.append(a.get('href'))
            return urls
        
        super().__init__(functionName, siteUrl, handler)   

class LearnviralHandler(PageSiteHandler):
    def __init__(self):
        functionName = 'LearnviralHandler'
        siteUrl = 'https://udemycoupon.learnviral.com/coupon-category/'\
            'free100-discount/'
        def handler(soup):
            return [
                a.get('href') for a in \
                soup.findAll('a', {
                    'class': 'coupon-code-link btn promotion'})]
        
        super().__init__(functionName, siteUrl, handler)        

# multiple page classes 
class SmartybroHandler(MultiPageSiteHandler):
    def __init__(self):
        functionName = 'SmartybroHandler'
        siteUrl = 'https://smartybro.com/category/udemy-coupon-100-off/'
        def mainHandlerFunc(soup):
            return [
                h2.find('a').get('href') for h2 in\
                soup.findAll('h2',{'class':'grid-tit'})]
        def couponHandlerFunc(soup):
            return soup.find(
                'a',
                {'class': 'fasc-button fasc-size-xlarge'\
                    ' fasc-type-flat'}).get('href').strip()
            
        super().__init__(functionName, siteUrl, mainHandlerFunc,
                         couponHandlerFunc)        

class OnlineTutorialsHandler(MultiPageSiteHandler):
    def __init__(self):
        functionName = 'OnlineTutorialsHandler'
        siteUrl = 'https://onlinetutorials.org'
        def mainHandlerFunc(soup):
            return [
                h2.find('a').get('href') for h2 in\
                soup.findAll('h2') if h2.find('a')]
        def couponHandlerFunc(soup):
            return soup.find(
                'a',
                {'class': 'btn_offer_block'\
                    ' re_track_btn'}).get('href').strip()
            
        super().__init__(functionName, siteUrl, mainHandlerFunc,
                         couponHandlerFunc)  

class BlazeCouponHandler(MultiPageSiteHandler):
    def __init__(self):
        functionName = 'BlazeCouponHandler'
        siteUrl = 'https://blazecoupon.com/'
        def mainHandlerFunc(soup):
            return [
                a.get('href') for a in\
                soup.findAll('a',
                             {'class':'btn_offer_block re_track_btn'})]
        def couponHandlerFunc(soup):
            return soup.find(
                'a',
                {'class': 'btn_offer_block'\
                    ' re_track_btn'}).get('href').strip()
            
        super().__init__(functionName, siteUrl, mainHandlerFunc,
                         couponHandlerFunc) 

class UdemyfreebiesHandler(MultiPageSiteHandler):
    def __init__(self):
        functionName = 'UdemyfreebiesHandler'
        siteUrl = 'https://www.udemyfreebies.com/'
        def mainHandlerFunc(soup):
            return [
                a.get('href') for a in\
                soup.findAll('a',{'class':'button-icon'})]
        def couponHandlerFunc(soup):
            return soup.find(
                'a',
                {'class': 'button-icon'}).get('href').strip()
            
        super().__init__(functionName, siteUrl, mainHandlerFunc,
                         couponHandlerFunc)  