'''
Functions for collection discount urls and course names
'''

import pandas as pd
import threading 

import types
import siteHandlers 

dbPath = 'DB.csv'

class CouponDB():
    db = pd.read_csv(dbPath)
    
    @classmethod
    def add(cls, url):
        if not (url in cls.db['url'].values):
            cls.db.loc[cls.db.shape[0]] = [url, True]

    @classmethod
    def filterNewCoupons(cls):
        return list(cls.db.loc[cls.db['recent'] == True,'url'].values)

    @classmethod
    def save(cls): 
        cls.db['recent'] = False
        cls.db.to_csv(dbPath, index=False)
        
    @classmethod
    def reset(cls): 
        cls.db = pd.DataFrame([],columns=['url','recent'])

def _checkValidUrl(url):
    return not('https://www.udemy.com/course/' in url and '?couponCode=' not in url)

def searchNewCoupons():
    siteHandlerList = []
    for a in dir(siteHandlers):
        attr =  getattr(siteHandlers, a)
        if isinstance(attr, type)\
            and attr not in [siteHandlers.SiteHandler,
                             siteHandlers.PageSiteHandler,
                             siteHandlers.MultiPageSiteHandler]\
            and (issubclass(attr, 
                    siteHandlers.PageSiteHandler)\
                or issubclass(attr, 
                    siteHandlers.MultiPageSiteHandler)):
            siteHandlerList.append(attr)  
    resultDict = {}
    threadList = [] 
    for HandlerClass in siteHandlerList:
        thread = threading.Thread(
            target=lambda: HandlerClass().returnUrls(resultDict),
            daemon=True)
        thread.start()
        threadList.append(thread)
    [thread.join() for thread in threadList]

    for _, result in resultDict.items():
        if isinstance(result, siteHandlers.SiteHandlerException):
            raise result
            return {}

    coupons = []
    for _, result in resultDict.items():
        coupons += [url for url in result if _checkValidUrl(url)]
    return coupons