'''
Functions for crawling discount data
'''

import requests 
from bs4 import BeautifulSoup

HEADERS = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) '\
                      'AppleWebKit/537.36 (KHTML, like Gecko) '\
                      'Chrome/51.0.2704.79 Safari/537.36'}

def _returnResults(resultDict,functionName, resultAux, ExceptionCls):
    resultDict[functionName] = resultAux
    if not resultAux:
        resultDict[functionName] = ExceptionCls(functionName)  

def getCouponsKeepercoupon(resultDict, ExceptionCls): 
    functionName = 'getCouponsKeepercoupon'
    url = 'https://keepercoupon.com/'
    resultAux = []
    try:
        r = requests.get(url, headers=HEADERS)
        soup = BeautifulSoup(r.text,'html.parser')
        urls = [
            a.get('href') for a in \
            soup.findAll(
                'a', 
                {'class': 'coupon-code-link button promotion'})]
        resultAux += urls
    except Exception as e:
        pass
    _returnResults(resultDict,functionName, resultAux, ExceptionCls)

def getCouponsDiscountsGlobal(resultDict, ExceptionCls): 
    functionName = 'getCouponsDiscountsGlobal'
    url = 'http://udemycoupon.discountsglobal.com/coupon-category/free-2/'
    resultAux = []
    try:
        r = requests.get(url, headers=HEADERS)
        soup = BeautifulSoup(r.text,'html.parser')
        for div in soup.findAll('div', {'class': 'item-panel'}):
            url = div.find('div', 
                           {'class': 'link-holder'}).find('a').get('href') 
            resultAux += [url]
    except Exception as e:
        pass
    _returnResults(resultDict,functionName, resultAux, ExceptionCls)

def getCouponsGuru99(resultDict, ExceptionCls): 
    functionName = 'getCouponsGuru99'
    url = 'https://www.guru99.com/free-udemy-course.html'
    resultAux = []
    try:
        r = requests.get(url, headers=HEADERS)
        soup = BeautifulSoup(r.text,'html.parser')
        
        urls = []
        for i, row in enumerate(soup.find('table').findAll('tr')):
            if i==0: continue 
            a = row.findAll('td')[1].find('a')
            urls.append(a.get('href'))
        resultAux += urls
    except Exception as e:
        pass
    _returnResults(resultDict,functionName, resultAux, ExceptionCls)

def getCouponsLearnviral(resultDict, ExceptionCls): 
    functionName = 'getCouponsLearnviral'
    url = 'https://udemycoupon.learnviral.com/coupon-category/'\
        'free100-discount/'
    resultAux = []
    try:
        r = requests.get(url, headers=HEADERS)
        soup = BeautifulSoup(r.text,'html.parser')
        urls = [
            a.get('href') for a in \
            soup.findAll('a', {'class': 'coupon-code-link btn promotion'})
        ]
        resultAux += urls
    except Exception as e:
        pass 
    _returnResults(resultDict,functionName, resultAux, ExceptionCls)

def getCouponsSmartybro(resultDict, ExceptionCls): 
    functionName = 'getCouponsSmartybro'
    url = 'https://smartybro.com/category/udemy-coupon-100-off/'
    resultAux = []
    try:
        r = requests.get(url, headers=HEADERS)
        soup = BeautifulSoup(r.text,'html.parser')
        
        url_list = [
            h2.find('a').get('href') for h2 in\
                soup.findAll('h2',{'class':'grid-tit'})]
        urls = []
        for url in url_list:
            r = requests.get(url, headers=HEADERS)
            soup = BeautifulSoup(r.text,'html.parser')
            a = soup.find(
                'a',
                {'class': 'fasc-button fasc-size-xlarge fasc-type-flat'})
            urls.append(a.get('href').strip())
        resultAux += urls
    except Exception as e:
        pass
    _returnResults(resultDict,functionName, resultAux, ExceptionCls)    

def getCouponsBlazecoupon(resultDict, ExceptionCls): 
    functionName = 'getCouponsBlazecoupon'
    url = 'https://blazecoupon.com/'
    resultAux = []
    try:
        r = requests.get(url, headers=HEADERS)
        soup = BeautifulSoup(r.text,'html.parser')
        
        url_list = [
            a.get('href') for a in\
                soup.findAll('a',{'class':'btn_offer_block re_track_btn'})]
        urls = []
        for url in url_list:
            r = requests.get(url, headers=HEADERS)
            soup = BeautifulSoup(r.text,'html.parser')
            a = soup.find(
                'a',
                {'class': 'btn_offer_block re_track_btn'})
            urls.append(a.get('href').strip())
        resultAux += urls
    except Exception as e:
        pass  
    _returnResults(resultDict,functionName, resultAux, ExceptionCls)

def getCouponsUdemyfreebies(resultDict, ExceptionCls): 
    functionName = 'getCouponsUdemyfreebies'
    url = 'https://www.udemyfreebies.com/'
    resultAux = []
    try:
        r = requests.get(url, headers=HEADERS)
        soup = BeautifulSoup(r.text,'html.parser')
        
        url_list = [
            a.get('href') for a in\
                soup.findAll('a',{'class':'button-icon'})]
        urls = []
        for url in url_list:
            r = requests.get(url, headers=HEADERS)
            soup = BeautifulSoup(r.text,'html.parser')
            a = soup.find(
                'a',
                {'class': 'button-icon'})
            urls.append(a.get('href').strip())
        resultAux += urls
    except Exception as e:
        pass  
    _returnResults(resultDict,functionName, resultAux, ExceptionCls)

def getCouponsOnlineTutorials(resultDict, ExceptionCls):
    functionName = 'getCouponsOnlineTutorials'
    url = 'https://onlinetutorials.org'
    resultAux = []
    try:
        r = requests.get(url, headers=HEADERS)
        soup = BeautifulSoup(r.text,'html.parser')
        
        url_list = [
            h2.find('a').get('href') for h2 in\
                soup.findAll('h2')]
        urls = []
        for url in url_list:
            r = requests.get(url, headers=HEADERS)
            soup = BeautifulSoup(r.text,'html.parser')
            a = soup.find(
                'a',
                {'class': 'btn_offer_block re_track_btn'})
            urls.append(a.get('href').strip())
        resultAux += urls
    except Exception as e:
        pass  
    _returnResults(resultDict,functionName, resultAux, ExceptionCls)