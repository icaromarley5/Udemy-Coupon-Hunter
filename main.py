
import logging
import time

import coupons 
import udemy 

import sys
#'''
logging.root.setLevel('INFO')

oldTime = time.time()

logging.info('Collecting coupons...')
urls = coupons.getCoupons()
if urls:
    logging.info(f'Coupons found: {len(urls)}')
    logging.info('Buying 100% off courses...')
    
    userData = None
    if len(sys.argv) == 3:
        userData = {
            'email': sys.argv[1],
            'password': sys.argv[2],}
    couponsBought = udemy.checkCourses(urls, userData)   
    if couponsBought != 'Fail':
        if couponsBought:
            logging.info(f'Coupons bought: {len(couponsBought)}')
        else:
            logging.info(f'No new coupons were available')
else:
    logging.info('No new coupons were found')

executionTime = (time.time() - oldTime)/60
logging.info(f'Done. Execution time: {executionTime:.1f} min')
#'''
'''
import pandas as pd 

urls = pd.read_csv('DB.csv')['url'].values
userData = {
            'email': sys.argv[1],
            'password': sys.argv[2],}
couponsBought = udemy.checkCourses(urls, userData) 
'''