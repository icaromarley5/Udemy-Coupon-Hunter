'''

Functions related to coupons

'''

from bs4 import BeautifulSoup
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import browsers
import re
from warning_errors import write_warning
import sites
import inspect



# login an password for Udemy acc
login = ""
password = ""
    
# call all coupon collect functions
# return discounts
def get_all_links(input_list=[1]):
    functions = inspect.getmembers(sites, inspect.isfunction)
    functions = [t[1] for t in functions if inspect.getmodule(t[1]) == sites]

    links = browsers.process_multi_tasks(functions,input_list)    
    return links
    
# get discounts and checks them 
def get_new_discounts():
    urls = get_all_links()
    print(len(urls), "urls found")
    
    # checks valid urls
    print("Checking urls")
    # filter duplicates and in the wrong format
    urls_aux = []
    for url in urls:
        if url not in urls_aux:
            pattern = r'https:\/\/www\.udemy\.com\/[^\/.]*\/'
            free = len(re.sub(pattern,'',url)) == 0
            if (not free):
                urls_aux.append(url)
    urls = urls_aux
    print(len(urls), "unique urls")
    # deep search for valid urls
    discounts_urls = browsers.process_multi_tasks([check_discounts],urls)
    
    print(len(discounts_urls), "valid urls")
    return discounts_urls
    
# checks valid discounts
# return discount list
def check_discounts(browser,input_list):
    discount_urls = []
    for url in input_list:
        browser.get(url)
        
        # deals with ads links
        if "https://udemycoupon.org/udemy/" in browser.current_url:#pagina intermediaria de propaganda
            try:
                wait = WebDriverWait(browser, 10)
                wait.until(lambda driver: driver.find_element_by_css_selector("a[class='btn btn-success btn-lg get-link']"))
                # click on button
                browser.find_element_by_css_selector("a[class='btn btn-success btn-lg get-link']").click()
                wait.until(lambda driver: "https://www.udemy.com/" in driver.current_url)
            except TimeoutException:# proceeds
                pass    
        
        html = browser.page_source
        soup = BeautifulSoup(html, 'html.parser')

        # checks if the discount is valid
        valid = False
        if "100% off" in soup.get_text():
            for tag in soup.findAll("span", { "data-purpose" : "discount-rate" }):
                if "100% off" in str(tag):#tag.contents[0]
                    valid = True
                    break      
            if not valid:
                text = "100 off and is not buyable " + url + "\n"
                write_warning(text)

        if valid: 
            discount_urls.append(browser.current_url)
    return discount_urls
    
def login_udemy(browser):
    global login, password
    url = "https://www.udemy.com/join/login-popup/"
    browser.get(url)
    username = browser.find_element_by_id("id_email")
    password = browser.find_element_by_id("id_password")
    username.send_keys(login)
    password.send_keys(password)
    browser.find_element_by_id("submit-id-submit").click()

# checks if course is already taken
def is_bought(url):
    return "/overview" in url

def check_bought(browser):
    try:
        wait = WebDriverWait(browser, 30)
        wait.until(lambda driver: is_bought(driver.current_url))
        return True
    except TimeoutException:
        return False

def setup_account(user,passw):
    global login,password
    login = user
    password = passw

def buy_discount_courses(urls):
    browsers.process_task(buy_discounts,urls)

def buy_discounts(browser, input_list=[]):
    urls = input_list
    print("Trying to log in to Udemy")
    login_udemy(browser)

    # tries to buy each discount
    courses = 0
    i2 = 1
    for url in urls:
        browser.get(url)
        if (check_bought(browser)):
            i2+=1
            continue
        
        html = browser.page_source
        bought = False
        button_text_list = ["Buy Now","Enroll Now"] # button types
        for button_text in button_text_list:
            if button_text in html:
                try:
                    browser.find_element_by_link_text(button_text).click()
                    
                    if 'https://www.udemy.com/cart/checkout/' in browser.current_url:
                        write_warning('Fail on buying '+browser.current_url + " " + url)
    
                    if not check_bought(browser):
                        try:
                            wait = WebDriverWait(browser, 10)
                            wait.until(lambda driver: "https://www.udemy.com/cart/success/" in browser.current_url)
                            #print(browser.current_url)
                        except TimeoutException:
                            print("You've successfully enrolled in" in browser.page_source)
                            print("Debug: please check html")
                            break
                    else:
                        print("Course is already taken")
                    courses+=1
                    bought = True                              
                except NoSuchElementException:
                    print("Debug: ",button_text," not found, please check", browser.current_url)
                        
        if not bought:
            text = "Buyable and couldn't buy" + browser.current_url + "\n"
            write_warning(text)
        
        i2+=1
   
    print(courses, "added to account")
    return [courses]