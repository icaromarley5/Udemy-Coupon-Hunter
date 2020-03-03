import unittest

import coupons 
import siteHandlers

import pandas as pd

import pyautogui
import udemy 

imagePath = 'udemyImgs/'

class TestCoupons(unittest.TestCase):
    def test_SearchNewCoupons(self):
        discounts = {}
        try:
            discounts = coupons.searchNewCoupons()
        except siteHandlers.SiteHandlerException as e:
            self.fail(f"Function {e} at search failed to get discount data")
        if not (discounts and isinstance(discounts,list)):
            self.fail(f'search failed to create discount data')
        if not all(map(coupons._checkValidUrl,discounts)):
            self.fail(f'search returned invalid urls')
    
class TestCouponDB(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        coupons.CouponDB.db = pd.DataFrame([],
            columns=['url','recent'])

    def tearDown(self):
        coupons.CouponDB.db = \
            coupons.CouponDB.db[
                ~ coupons.CouponDB.db['url'].isin(
                    ['test', 'test2'])]
              
    def test_CouponDBAdd(self):
        coupons.CouponDB.add('test')
        row = coupons.CouponDB.db[
            coupons.CouponDB.db['url'] == 'test'].iloc[0]
        self.assertTrue(row['recent'])
        
        coupons.CouponDB.db.loc[
            coupons.CouponDB.db.shape[0]] = [
                'test2', False]
        coupons.CouponDB.add('test2')
        row = coupons.CouponDB.db[
            coupons.CouponDB.db['url'] == 'test2'].iloc[0]
        self.assertFalse(row['recent'])

    def test_CouponDBFilter(self):
        coupons.CouponDB.db.loc[
            coupons.CouponDB.db.shape[0]] = ['test', False]
        coupons.CouponDB.add('test2')
        row = coupons.CouponDB.db[
            coupons.CouponDB.db['url'] == 'test'].iloc[0]
        self.assertFalse(row['recent'])
        couponData = coupons.CouponDB.filterNewCoupons()
        self.assertFalse('test' in couponData)
        self.assertTrue('test2' in couponData)
        
    def test_CouponDBReset(self):
        coupons.CouponDB.add('test')
        row = coupons.CouponDB.db[
            coupons.CouponDB.db['url'] == 'test'].iloc[0]
        self.assertFalse(row.empty)
        coupons.CouponDB.reset()
        self.assertTrue(coupons.CouponDB.db.empty)
                                
if __name__ == '__main__':
    unittest.main()