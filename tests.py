import unittest

import coupons 

import pandas as pd

import pyautogui
import udemy 

imagePath = 'udemyImgs/'

class TestCoupons(unittest.TestCase):
    def test_getCoupons(self):
        discounts = {}
        try:
            discounts = coupons.getCoupons(save=False)
        except coupons.FunctionException as e:
            self.fail(f"Function {e} at getCoupons failed to get discount data")
        if not (discounts and isinstance(discounts,list)):
            self.fail(f'getCoupons failed to create discount data')
        if not all(map(coupons.checkValidUrl,discounts)):
            self.fail(f'getCoupons returned invalid urls')
    
class TestCouponCache(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        coupons.CouponCache.cache = pd.DataFrame([],
            columns=['url','recent'])

    def tearDown(self):
        coupons.CouponCache.cache = \
            coupons.CouponCache.cache[
                ~ coupons.CouponCache.cache['url'].isin(
                    ['test', 'test2'])]
              
    def test_CouponCacheAdd(self):
        coupons.CouponCache.add('test')
        row = coupons.CouponCache.cache[
            coupons.CouponCache.cache['url'] == 'test'].iloc[0]
        self.assertEqual(True, row['recent'])
        
        coupons.CouponCache.cache.loc[
            coupons.CouponCache.cache.shape[0]] = [
                'test2', False]
        coupons.CouponCache.add('test2')
        row = coupons.CouponCache.cache[
            coupons.CouponCache.cache['url'] == 'test2'].iloc[0]
        self.assertEqual(False, row['recent'])

    def test_CouponCacheFilter(self):
        coupons.CouponCache.cache.loc[
            coupons.CouponCache.cache.shape[0]] = ['test', False]
        coupons.CouponCache.add('test2')
        row = coupons.CouponCache.cache[
            coupons.CouponCache.cache['url'] == 'test'].iloc[0]
        self.assertEqual(False, row['recent'])
        couponData = coupons.CouponCache.filterOldCoupons()
        self.assertTrue(
            couponData[couponData['url'] == 'test'].empty)
        self.assertFalse(
            couponData[
                couponData['url'] == 'test2'].empty)

    def test_GetCoupons(self):
        couponsList = coupons.CouponCache.getCoupons()
        self.assertTrue('test' not in couponsList)
        coupons.CouponCache.add('test')
        couponsList = coupons.CouponCache.getCoupons()
        self.assertTrue(isinstance(couponsList, list))
        self.assertTrue('test' in couponsList)
        
if __name__ == '__main__':
    unittest.main()