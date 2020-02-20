'''
Functions for collection discount urls and course names
'''

import pandas as pd
import threading 

import types
import siteFunctions 

cachePath = 'cache.csv'

class CouponCache():
    cache = pd.read_csv(cachePath)
    
    @classmethod
    def add(cls, url):
        if not (url in cls.cache['url'].values):
            cls.cache.loc[cls.cache.shape[0]] = [url, True]

    @classmethod
    def filterOldCoupons(cls):
        return cls.cache[cls.cache['recent'] == True]

    @classmethod
    def save(cls): 
        cls.cache['recent'] = False
        cls.cache.to_csv(cachePath, index=False)

    @classmethod
    def getCoupons(cls): 
        return list(cls.filterOldCoupons()['url'].values)
           
class FunctionException(Exception):
    pass

def getCoupons(save=True):
    siteFunctionList = [
        getattr(siteFunctions, a) for a in dir(siteFunctions)
            if isinstance(getattr(
                siteFunctions, a),
                types.FunctionType) and not a.startswith('_')]

    resultDict = {}
    threadList = [] 
    for f in siteFunctionList:
        thread = threading.Thread(target=f,
                                  args=[
                                      resultDict, 
                                      FunctionException],
                                  daemon=True)
        thread.start()
        threadList.append(thread)
    [thread.join() for thread in threadList]

    for _, result in resultDict.items():
        if isinstance(result, FunctionException):
            raise result
            return {}

    for _, result in resultDict.items():
        urlList = [CouponCache.add(url) for url in result if checkValidUrl(url)]
    coupons = CouponCache.getCoupons()
    if save:
        CouponCache.save()
    return coupons

def checkValidUrl(url):
    return not('https://www.udemy.com/course/' in url and '?couponCode=' not in url)