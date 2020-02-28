from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.chrome.options import Options

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

import logging 

waitTime = 1 # 3 5 15

def openBrowser():
    options = Options()
    options.add_argument('start-maximized')
    options.add_experimental_option('excludeSwitches', ['enable-automation'])
    options.add_experimental_option('useAutomationExtension', False)    
    options.add_argument('--log-level=3')  
    options.add_argument('disable-gpu')  
    options.add_argument("--lang=en-US")
    browser = WebDriver('./chromedriver', options=options) 
    browser.execute_cdp_cmd('Page.addScriptToEvaluateOnNewDocument', {
    'source': '''
        Object.defineProperty(navigator, 'webdriver', {
        get: () => undefined
        })
    '''
    })
    browser.execute_cdp_cmd('Network.enable', {})
    browser.execute_cdp_cmd(
        'Network.setExtraHTTPHeaders',
        {'headers': {'User-Agent': 'browser1'}})
    return browser   

class UdemyRobotException(Exception):
    pass 

def checkUdemy(browser):
    if 'Please verify you are a human' in browser.page_source:
        logging.critical('''
            Selenium was blocked by Udemy.
            Please pass the human test.
            Press ENTER to continue''')
        input()
        try:
            WebDriverWait(browser, waitTime * 5).until(lambda:
                'Please verify you are a human' not in browser.page_source)
            return True
        except Exception as e:
            logging.execption(e)
            raise UdemyRobotException("You didn't pass the robot check")
   
def login(browser, email, password):
    try:
        browser.get('https://www.udemy.com/join/login-popup/?locale=pt_BR&response_type=html&next=https%3A%2F%2Fwww.udemy.com%2F')
        browser.implicitly_wait(waitTime * 2)
        checkUdemy(browser)
        browser.find_element_by_id('email--1').send_keys(email)
        browser.find_element_by_id('id_password').send_keys(password)
        browser.find_element_by_id('submit-id-submit').click()
        browser.implicitly_wait(waitTime * 2)
        checkUdemy(browser)
        return True
    except Exception as e:
        if isinstance(e, UdemyRobotException): raise e
        return False

def buyCourse(browser, url):
    success = False 
    try:
        WebDriverWait(browser, waitTime * 10).until(
            EC.presence_of_element_located((
                By.XPATH, 
                '//div[@class="slider-menu"]//button[. = "Enroll now"]'))).click()
    except Exception as e:
        try:
            WebDriverWait(browser, waitTime * 10).until(
                EC.presence_of_element_located((
                    By.CLASS_NAME, 
                    'course-cta'))).click()
        except Exception as e:
            logging.critical("Course wasn't bought")
            import pdb;pdb.set_trace()
    browser.implicitly_wait(waitTime * 3)
    return success

def checkCourse(browser, url):
    free = False 
    try:
        browser.get(url)
        browser.implicitly_wait(waitTime * 2)
        checkUdemy(browser)   
        currentUrl = browser.current_url
        if 'https://www.udemy.com/course/' in currentUrl\
            and 'couponCode=' in currentUrl:
            WebDriverWait(browser, waitTime * 10).until(
                EC.presence_of_element_located((
                    By.XPATH, 
                    '//div[@class="buy-box"]//span[contains(text(),"100% off")]')))
            free = True 
        if "100% off" in browser.page_source and not free:
            print('100 off',url, 'https://www.udemy.com/course/' in currentUrl and 'couponCode=' in currentUrl)
            print(currentUrl)
            import pdb;pdb.set_trace()
    except Exception as e:
        if isinstance(e, UdemyRobotException): raise e
        if '100% off' in browser.page_source:
            logging.critical('100% off in html but the check failed')
            import pdb;pdb.set_trace()
    browser.implicitly_wait(waitTime * 3)
    return free

def checkCourses(urlList, userData=None):
    coursesBought = []
    
    browser = openBrowser()
    loginResult = False
    
    try:
        if userData:
            loginResult = login(
                browser, 
                userData['email'], 
                userData['password'])
        for url in urlList: 
            checkResult = checkCourse(browser, url) 
            if loginResult and checkResult and buyCourse(browser, url):
                coursesBought.append(url)           
    except Exception as e:
        logging.warning('An exception halted the execution')
        logging.warning(e)
        return 'Fail'
    finally:
        browser.close()
    return coursesBought