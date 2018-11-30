'''

Main script. Run the file and insert your account details 
The code will search the newest free coupons and buy them for you
There is no risk of spending money since it requires payout info 
and the crawler only presses the Udemy's "buy now" button

'''

import coupons_utils

'''
print("Udemy Coupon Hunter. Please insert your Udemy account")
print("Login:")
login = str(input())
print("Password:")
password = str(input())
'''
print("Execution started")

print("Collecting discounts")

urls = coupons_utils.get_new_discounts()
print(len(urls)," discounts found")
# write in file
with open('urls.txt','w') as file:
    for url in urls:
        file.write(url+'\n')