
import logging

import coupons 
import udemy 

urls = coupons.getCoupons()
if urls:
    udemy.buyCourses(urls)
else:
    logging.info('No new coupons were found')

#import pandas as pd 
#udemy.buyCourses(pd.read_csv('cache.csv')['url'].values)