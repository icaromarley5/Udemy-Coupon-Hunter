'''
Functions focused on crawling discount data

    #listas de sites com selenium
    listas de sites com requests  '''

import requests 
from bs4 import BeautifulSoup

HEADERS = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) '\
                      'AppleWebKit/537.36 (KHTML, like Gecko) '\
                      'Chrome/51.0.2704.79 Safari/537.36'}

def getCouponsDiscountsGlobal(resultDict, ExceptionCls): 
    url = 'http://udemycoupon.discountsglobal.com/coupon-category/free-2/'
    resultAux = {}
    try:
        r = requests.get(url, headers=HEADERS)
        soup = BeautifulSoup(r.text,'html.parser')
        for div in soup.findAll('div', {'class': 'item-panel'}):
            name = div.find('h3').find('a').text 
            name = name.replace('Discount: 100% off – ', '')
            name = name.replace('Discount: 75% off – ', '')
            name = name.replace('100% off ', '')
            url = div.find('div', 
                           {'class': 'link-holder'}).find('a').get('href') 
            resultAux.update({url.strip(): name.strip()})
    except Exception as e:
        raise ExceptionCls('getCouponsDiscountsGlobal')
    
    if not resultAux:
        raise ExceptionCls('getCouponsDiscountsGlobal')
    
    resultDict.update(resultAux)

def getCouponsGuru99(resultDict, ExceptionCls): 
    url = 'https://www.guru99.com/free-udemy-course.html'
    resultAux = {}
    try:
        r = requests.get(url, headers=HEADERS)
        soup = BeautifulSoup(r.text,'html.parser')
        
        urls = []
        titles = []
        for i, row in enumerate(soup.find('table').findAll('tr')):
            if i==0: continue 
            a = row.findAll('td')[1].find('a')
            titles.append(a.text)
            urls.append(a.get('href'))

        resultAux.update(
            {url.strip():name.strip() for (url,name) in zip(urls,titles)})
    except Exception as e:
        raise e 
        raise ExceptionCls('getCouponsGuru99')  
    if not resultAux:
        raise ExceptionCls('getCouponsGuru99')
    
    resultDict.update(resultAux)

def getCouponsLearnviral(resultDict, ExceptionCls): 
    url = 'https://udemycoupon.learnviral.com/coupon-category/'\
        'free100-discount/'
    resultAux = {}
    try:
        r = requests.get(url, headers=HEADERS)
        soup = BeautifulSoup(r.text,'html.parser')
        titles = [
            title.text.replace('[Free]', '') for title in \
            soup.findAll('h3', {'class': 'entry-title'})
        ]
        urls = [
            a.get('href') for a in \
            soup.findAll('a', {'class': 'coupon-code-link btn promotion'})
        ]
        resultAux.update(
            {url.strip():name.strip() for (url,name) in zip(urls,titles)})
    except Exception as e:
        raise ExceptionCls('getCouponsLearnviral')  
    if not resultAux:
        raise ExceptionCls('getCouponsLearnviral')
    
    resultDict.update(resultAux)
'''
def getCouponsOnlineTutorials(resultDict, ExceptionCls):
    url = 'https://onlinetutorials.org'
    resultAux = {}
    try:
        r = requests.get(url, headers=HEADERS)
        soup = BeautifulSoup(r.text,'html.parser')
        titles = [
            title.find('a').text for title in \
            soup.findAll('h3', {'class': 'entry-title'})
        ]
        urls = [
            a.get('href') for a in \
            soup.findAll('a', {'class': 'coupon-code-link button promotion'})
        ]
        resultAux.update(
            {url.strip(): name.strip() for (url,name) in zip(urls,titles)})
    except Exception as e:
        raise ExceptionCls('getCouponsOnlineTutorials')  
    
    if not resultAux:
        raise ExceptionCls('getCouponsOnlineTutorials')
    
    resultDict.update(resultAux)
'''