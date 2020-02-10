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
    def add(cls, row):
        if not (row['url'] in cls.cache['url'].values):
            cls.cache.loc[cls.cache.shape[0]] = [row['name'], row['url'],True]

    @classmethod
    def filterOldCoupons(cls):
        return cls.cache[cls.cache['recent'] == True]

    @classmethod
    def save(cls): 
        cls.cache['recent'] = False
        cls.cache.to_csv(cachePath, index=False)

    @classmethod
    def getCoupons(cls): 
        return cls.filterOldCoupons().set_index(
            'url')['name'].to_dict()
           
class FunctionException(Exception):
    pass

def getCoupons():
    siteFunctionList = [
        getattr(siteFunctions, a) for a in dir(siteFunctions)
            if isinstance(getattr(
                siteFunctions, a),
                types.FunctionType)]

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

    resultDict = {url:name\
        for (url, name) in resultDict.items() if checkValidUrl(url)}   
    return resultDict

def checkValidUrl(url):
    return not('https://www.udemy.com/course/' in url and '?couponCode=' not in url)

def printCoupons():
    coupons = getCoupons()
    
    for url, name in coupons.items():
        CouponCache.add({'name': name, 'url': url})
    
    coupons = CouponCache.getCoupons()
    
    for url, name in coupons.items():
        print(f'Name: {name}\nURL: {url}\n')
    if not coupons.items():
        print('There are no new coupons')
    CouponCache.save()