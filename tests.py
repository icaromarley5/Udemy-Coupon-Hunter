import unittest

import coupons 
import siteHandlers

import pandas as pd

import pyautogui
import udemy 

imagePath = 'udemyImgs/'

class TestCoupons(unittest.TestCase):
    def test_getCoupons(self):
        discounts = {}
        try:
            discounts = coupons.getCoupons(save=False)
        except siteHandlers.SiteHandlerException as e:
            self.fail(f"Function {e} at getCoupons failed to get discount data")
        if not (discounts and isinstance(discounts,list)):
            self.fail(f'getCoupons failed to create discount data')
        if not all(map(coupons.checkValidUrl,discounts)):
            self.fail(f'getCoupons returned invalid urls')
    
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
        self.assertEqual(True, row['recent'])
        
        coupons.CouponDB.db.loc[
            coupons.CouponDB.db.shape[0]] = [
                'test2', False]
        coupons.CouponDB.add('test2')
        row = coupons.CouponDB.db[
            coupons.CouponDB.db['url'] == 'test2'].iloc[0]
        self.assertEqual(False, row['recent'])

    def test_CouponDBFilter(self):
        coupons.CouponDB.db.loc[
            coupons.CouponDB.db.shape[0]] = ['test', False]
        coupons.CouponDB.add('test2')
        row = coupons.CouponDB.db[
            coupons.CouponDB.db['url'] == 'test'].iloc[0]
        self.assertEqual(False, row['recent'])
        couponData = coupons.CouponDB.filterOldCoupons()
        self.assertTrue(
            couponData[couponData['url'] == 'test'].empty)
        self.assertFalse(
            couponData[
                couponData['url'] == 'test2'].empty)

    def test_GetCoupons(self):
        couponsList = coupons.CouponDB.getCoupons()
        self.assertTrue('test' not in couponsList)
        coupons.CouponDB.add('test')
        couponsList = coupons.CouponDB.getCoupons()
        self.assertTrue(isinstance(couponsList, list))
        self.assertTrue('test' in couponsList)
        
if __name__ == '__main__':
    unittest.main()