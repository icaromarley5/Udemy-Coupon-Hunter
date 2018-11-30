'''

Site specific crawling functions


'''
import inspect
from bs4 import BeautifulSoup
from warning_errors import write_warning

def get_all_realdiscount_links(browser,input_list = [1]):
    base = "https://www.real.discount/new/page/"
    links = []

    for counter in input_list:
        url = base + str(counter)+'/'

        browser.get(url)
        html = browser.page_source
        soup = BeautifulSoup(html, 'html.parser')

        for header in soup.findAll('div', {'class' : 'embed-responsive'}):
            link = header.findAll('a')[0]
            links.append(link.get("href"))  

    urls = []
    for link in links:
        browser.get(link)
        html = browser.page_source
        soup = BeautifulSoup(html, 'html.parser')
        
        for url in soup.findAll('a',text='Get Coupon'):
            urls.append((url.get("href"))) 
    if urls == []:
        func_name = inspect.stack()[0][3]
        write_warning(func_name+' \n')  
    return urls 

def get_all_coupontry_links(browser,input_list = [1]):
    base = "https://coupontry.com/coupon-tag/100-off-udemy-coupon/page/"
    links = []

    for counter in input_list:
        url = base + str(counter)+'/'

        browser.get(url)
        html = browser.page_source
        soup = BeautifulSoup(html, 'html.parser')

        for header in soup.findAll('h3', {'class' : 'entry-title'}):
            link = header.findAll('a')[0]
            links.append(link.get("href"))  

    urls = []
    for link in links:
        browser.get(link)
        html = browser.page_source
        soup = BeautifulSoup(html, 'html.parser')
        
        for url in soup.findAll('a', {'data-clipboard-text' : 'Click to Redeem'}):
            urls.append((url.get("href"))) 
    if urls == []:
        func_name = inspect.stack()[0][3]
        write_warning(func_name+' \n')  
    return urls 
    
def get_all_yourhelpline_links(browser,input_list=[1]):
    base = "http://udemycoupon.yourhelpline.net/coupon-tag/udemy-100-off/page/"

    links = []
    for counter in input_list:
        url = base + str(counter)+'/'
        
        browser.get(url)
        html = browser.page_source
        soup = BeautifulSoup(html, 'html.parser')
        for link in soup.findAll('a', {'title' : 'Click to open site'}):
            links.append((link.get("href")))  

    urls = links
    if urls == []:
        func_name = inspect.stack()[0][3]
        write_warning(func_name+' \n')     
    return urls
    
def get_all_promocoupons24_links(browser,input_list=None):
    base = "http://www.promocoupons24.com/"
    links = []
    url = base

    browser.get(url)
    browser.find_element_by_id("popupContactClose").click()
    
    html = browser.page_source
    soup = BeautifulSoup(html, 'html.parser')

    for header in soup.findAll('div', {'class' : 'post-body entry-content'}):
        link = header.findAll('a')[0]
        links.append(link.get("href"))  
    print(links)
    urls = []
    for link in links:
        browser.get(link)
        html = browser.page_source
        soup = BeautifulSoup(html, 'html.parser')
        
        for url in soup.findAll('a'):
            if url.get("href") and "www.udemy.com/"  in url.get("href"):
                urls.append((url.get("href"))) 
        
    if urls == []:
        func_name = inspect.stack()[0][3]
        write_warning(func_name+' \n')    
    return urls 

def get_all_buzzudemy_links(browser,input_list = [1]):
    base = "https://buzzudemy.com/coupons-category/100-off-udemy-coupon/page/"
    links = []
    
    for counter in input_list:
        url = base + str(counter)+'/'
        browser.get(url)
        html = browser.page_source
        soup = BeautifulSoup(html, 'html.parser')
        for url in soup.findAll('a', {'class' : 'coupon_deal_URL'}):
            links.append(url.get("href"))  
    urls = links

    if urls == []:
        func_name = inspect.stack()[0][3]
        write_warning(func_name+' \n')  

    return urls  

def get_all_scrollcoupons_links(browser,input_list = [1]):
    base = "http://www.scrollcoupons.com/search/label/100%25%20discount"
    links = []
    url = base 
    browser.get(url)
    html = browser.page_source
    soup = BeautifulSoup(html, 'html.parser')
    
    for header in soup.findAll('h3', {'class' : 'item-title'}):
        link = header.findAll('a')[0]
        links.append(link.get("href"))  

    urls = []
    for link in links:
        browser.get(link)
        html = browser.page_source
        soup = BeautifulSoup(html, 'html.parser')
        
        for url in soup.findAll('a'):
            url_str = url.get("href")
            if url_str and "https://www.udemy.com" in url_str:
                urls.append(url_str)  

    if urls == []:
        func_name = inspect.stack()[0][3]
        write_warning(func_name+' \n')  

    return urls    


def get_all_anycouponcode_links(browser,input_list = [1]):
    base = "http://www.anycouponcode.net/tag/100-off/page/"
    final = "/?sort=newest"
    links = []
    url = base 
    html = browser.page_source
    soup = BeautifulSoup(html, 'html.parser')

    for counter in input_list:
        url = base + str(counter) + final
        browser.get(url)
        html = browser.page_source
        soup = BeautifulSoup(html, 'html.parser')
        
        for link in soup.findAll('a'):
            link_str = link.get("href")
            if link_str and "https://www.udemy.com" in link_str:
                links.append(link_str)  
    urls = links
    if urls == []:
        func_name = inspect.stack()[0][3]
        write_warning(func_name+' \n')  

    return urls    

def get_all_freeoncourses_links(browser,input_list = [1]):
    base = "http://www.freeoncourses.com/"
    links = []
    url = base 
    browser.get(url)
    html = browser.page_source
    soup = BeautifulSoup(html, 'html.parser')

    for header in soup.findAll('h2', {'class' : 'post-title entry-title'}):
        link = header.findAll('a')[0]
        links.append(link.get("href"))  

    urls = []
    for link in links:
        browser.get(link)
        html = browser.page_source
        soup = BeautifulSoup(html, 'html.parser')
        
        next_div = False
        for post in soup.findAll('div', {'class' : 'separator'}):
            if "100% Off Limited Time Offer." in post.text:
                next_div = True
                continue
            if next_div:
                urls_aux = post.findAll('a')
                if urls_aux == []:
                    continue
                url = urls_aux[0]
                urls.append((url.get("href"))) 
                break
    if urls == []:
        func_name = inspect.stack()[0][3]
        write_warning(func_name+' \n')  

    return urls    

def get_all_medium_links(browser,input_list = None):
    base = "https://medium.com/100-free-udemy-coupons"
    links = []
    url = base
    browser.get(url)
    html = browser.page_source
    soup = BeautifulSoup(html, 'html.parser')

    for link in soup.findAll('a', {'class' : 'u-block'}):
        links.append(link.get("href"))  

    urls = []
    for link in links:
        browser.get(link)
        html = browser.page_source
        soup = BeautifulSoup(html, 'html.parser')
        
        for url in soup.findAll('a', {'class' : 'markup--anchor markup--p-anchor'}):
            if (url.text =='Take this course!'):
                urls.append((url.get("href"))) 
                break
    if urls == []:
        func_name = inspect.stack()[0][3]
        write_warning(func_name+' \n')  
    return urls     

def get_all_udemycouponorg_links(browser,input_list = [1]):
    base = "https://udemycoupon.org/coupon-category/100-off-udemy-coupon/page/"
    links = []

    for counter in input_list:
        url = base + str(counter)+'/'

        browser.get(url)
        html = browser.page_source
        soup = BeautifulSoup(html, 'html.parser')

        for header in soup.findAll('h3', {'class' : 'entry-title'}):
            link = header.findAll('a')[0]
            links.append(link.get("href"))  

    urls = []
    for link in links:
        browser.get(link)
        html = browser.page_source
        soup = BeautifulSoup(html, 'html.parser')
        
        for url in soup.findAll('a', {'data-clipboard-text' : 'Click to Redeem'}):
            urls.append((url.get("href"))) 
    if urls == []:
        func_name = inspect.stack()[0][3]
        write_warning(func_name+' \n')  
    return urls     

def get_all_udemycoupon_links(browser,input_list=[1]):
    base = "http://udemycoupon.discountsglobal.com/coupon-category/free-2/page/"
    links = []
    for counter in input_list:
        url = base + str(counter)+'/'
        browser.get(url)                
        html = browser.page_source
        soup = BeautifulSoup(html, 'html.parser')
        for link in soup.findAll('a'):
            if link.get("title")!= None and "Click to " in link.get("title"):
                links.append((link.get("href")))  

    urls = links
    if urls == []:
        func_name = inspect.stack()[0][3]
        write_warning(func_name+' \n')  
    
    return urls    
   
def get_all_freeudemycourses_links(browser,input_list = None):
    base = "https://www.freeudemycourses.info/"
    links = []
    url = base

    browser.get(url)
    html = browser.page_source
    soup = BeautifulSoup(html, 'html.parser')

    for header in soup.findAll('h2', {'class' : 'post-title entry-title'}):
        link = header.findAll('a')[0]
        links.append(link.get("href"))  

    urls = []
    for link in links:
        browser.get(link)
        html = browser.page_source
        soup = BeautifulSoup(html, 'html.parser')
        
        for div in soup.findAll('div', {'class' : 'separator'}):
            urls_aux = div.findAll('a')
            if urls_aux == []:
                continue
            link = urls_aux[0]
            urls.append(link.get("href"))  

    if urls == []:
        func_name = inspect.stack()[0][3]
        write_warning(func_name+' \n')  
    return urls     



def get_all_onlinecoursesupdate_links(browser,input_list = None):
    base = "http://www.onlinecoursesupdate.com/"
    links = []
    url = base
        
    browser.get(url)
    html = browser.page_source
    soup = BeautifulSoup(html, 'html.parser')
    for header in soup.findAll('h3', {'class' : 'post-title entry-title'}):
        link = header.findAll('a')[0]
        links.append(link.get("href"))  
    
    urls = []
    for link in links:
        browser.get(link)
        html = browser.page_source
        soup = BeautifulSoup(html, 'html.parser')
        for link in soup.findAll('a'):
            if "Take This Course"  in link.contents:
                urls.append((link.get("href"))) 

    if urls == []:
        func_name = inspect.stack()[0][3]
        write_warning(func_name+' \n')  
    return urls

def get_all_learnviral_links(browser,input_list=[1]):
    base = "http://udemycoupon.learnviral.com/coupon-category/free100-discount/page/"

    links = []
    for counter in input_list:
        url = base + str(counter)+'/'
        
        browser.get(url)
        html = browser.page_source
        soup = BeautifulSoup(html, 'html.parser')
        for link in soup.findAll('a', {'title' : 'Click to open site'}):
            links.append((link.get("href")))  

    urls = links
    if urls == []:
        func_name = inspect.stack()[0][3]
        write_warning(func_name+' \n')       
    return urls
