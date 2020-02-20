from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.chrome.options import Options

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

import loginInfo 

import logging

waitTime = 5 # 15

def openBrowser(visible=False):
    options = Options()
    
    options.add_argument("start-maximized")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)    
    if not visible:
        options.add_argument("--headless")
        options.add_argument("--window-size=1366x1280")
        options.add_argument('log-level=2')
    browser = WebDriver('./chromedriver', options=options) 
    browser.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
    "source": """
        Object.defineProperty(navigator, 'webdriver', {
        get: () => undefined
        })
    """
    })
    browser.execute_cdp_cmd("Network.enable", {})
    browser.execute_cdp_cmd(
        "Network.setExtraHTTPHeaders",
        {"headers": {"User-Agent": "browser1"}})
    return browser   

def checkRobot(browser):
    if 'Please verify you are a human' in browser.page_source:
        logging.critical('''
            Selenium was blocked by Udemy.
            Please pass the human test.
            Press anything + ENTER to continue''')
        input()
        
def login(browser, email, password):
    try:
        browser.get('https://www.udemy.com/join/login-popup/?locale=pt_BR&response_type=html&next=https%3A%2F%2Fwww.udemy.com%2F')
        browser.implicitly_wait(waitTime * 2)
        checkRobot(browser)
        browser.find_element_by_id('email--1').send_keys(loginInfo.email)
        browser.find_element_by_id('id_password').send_keys(loginInfo.password)
        browser.find_element_by_id('submit-id-submit').click()
        browser.implicitly_wait(waitTime * 2)
        checkRobot(browser)
        return True
    except Exception as e:
        raise e
        return False

def buyCourse(browser, url):
    browser.get(url)
    browser.implicitly_wait(waitTime * 2)
    checkRobot(browser)
    success = False 
    try:
        buyBox = browser.find_element_by_xpath('//div[@class="buy-box"]')
        WebDriverWait(buyBox, waitTime * 4).until(
            EC.presence_of_element_located((
                By.XPATH, 
                '//span[contains(text(),"100% off")]')))
        try:
            WebDriverWait(buyBox, waitTime * 4).until(
            EC.presence_of_element_located((
                By.XPATH, 
                '//div[@class="slider-menu"]//button[. = "Enroll now"]'))).click()
        except:
            browser.find_element_by_class_name('course-cta').click()
        success = True 
    except Exception as e:
        if '100% off' in browser.page_source:
            logging.warning(e)
            logging.critical("Course wasn't bought")
            #WebDriverWait(buyBox, waitTime * 4).until(EC.presence_of_element_located((By.XPATH, '//div[@class="slider-menu"]//button[. = "Enroll now"]')))
            import pdb;pdb.set_trace()
    browser.implicitly_wait(waitTime * 3)
    return success

def buyCourses(urlList):
    browser = openBrowser(True)
    if login(browser, loginInfo.email, loginInfo.password):
        for url in urlList: 
            buyCourse(browser, url) 
    browser.close()
    
if __name__ == '__main__':
    urls = []
    buyCourses(urls)