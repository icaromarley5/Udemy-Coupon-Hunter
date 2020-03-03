
import logging
import time

import coupons 
import udemy 

import sys

#'''
logging.root.setLevel('INFO')

if len(sys.argv) < 3:
    raise Exception('Login data is needed')
userData = {
    'email': sys.argv[1],
    'password': sys.argv[2],}

if len(sys.argv) > 3 and 'reset' == sys.argv[3]:
    coupons.CouponDB.reset()
    
oldTime = time.time()

logging.info('Collecting coupons...')

urls = coupons.searchNewCoupons()
[coupons.CouponDB.add(url) for url in urls]
newCoupons = coupons.CouponDB.filterNewCoupons() 

if newCoupons:
    logging.info(f'Coupons found: {len(newCoupons)}')
    logging.info('Buying 100% off courses...')
    
    couponsBought = udemy.buyCourses(newCoupons, userData)   
    if couponsBought == 'Fail':
        logging.critical('Execution failed')
    elif couponsBought == 'Login Fail':
        logging.critical("Login failed")
    else:
        if not couponsBought:
            logging.info(f'No new coupons were available')
        else:
            logging.info(f'Coupons bought: {len(couponsBought)}')
        coupons.CouponDB.save()             
else:
    logging.info('No new coupons were found')

executionTime = (time.time() - oldTime)/60
logging.info(f'Completed. Execution time: {executionTime:.1f} min')
#'''
'''
import pandas as pd 

urls = pd.read_csv('DB.csv')['url'].values
userData = {
            'email': sys.argv[1],
            'password': sys.argv[2],}
couponsBought = udemy.buyCourses(urls, userData) 
'''