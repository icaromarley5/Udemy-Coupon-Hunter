from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.chrome.options import Options

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC

import logging 
import pdb

import userWarnings

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
    try:
        WebDriverWait(browser, 5).until(lambda browser:
                'Please verify you are a human' in browser.page_source)
        logging.critical('''
            Selenium was blocked by Udemy.
            Please pass the human test.
            Press ENTER to continue''')
        userWarnings.alertUser(
            'Selenium was blocked', 
            'Please check the CMD')
        input()
        try:
            WebDriverWait(browser, 10).until(lambda browser:
                'Please verify you are a human' not in browser.page_source)
            return True
        except Exception as e:
            logging.execption(e)
            raise UdemyRobotException("You didn't pass the robot check")
    except:
        return True
   
def login(browser, email, password):
    try:
        browser.get('https://www.udemy.com/join/login-popup/?locale=pt_BR&response_type=html&next=https%3A%2F%2Fwww.udemy.com%2F')
        checkUdemy(browser)
        browser.find_element_by_id('email--1').send_keys(email)
        browser.find_element_by_id('id_password').send_keys(password)
        browser.find_element_by_id('id_password').send_keys(Keys.RETURN)
        checkUdemy(browser)
        WebDriverWait(browser, 5).until(
            lambda browser: 
                'My courses' in browser.page_source)
        return True
    except Exception as e:
        if isinstance(e, UdemyRobotException): raise e
        #raise e
        logging.critical('Login attempt failed')
        return False


def buyCourse(browser):
    try:
        buyButton = WebDriverWait(browser, 20).until(
        EC.element_to_be_clickable((
            By.XPATH, 
            '//button[@class="course-cta btn btn-lg btn-quaternary btn-block"]'\
                '|(//div[@class="buy-box"]//button[. = "Enroll now"])[2]')))
        buyButton.click()
    except Exception as e:
        userWarnings.alertUser(
            "Course wasn't bought", 
            'Please check the CMD')
        pdb.set_trace()
    browser.implicitly_wait(5)

def checkCourse(browser, url):
    free = False 
    try:
        browser.get(url)
        checkUdemy(browser)   
        currentUrl = browser.current_url
        if 'https://www.udemy.com/course/' in currentUrl\
            and 'couponCode=' in currentUrl:
            WebDriverWait(browser, 10).until(
                EC.presence_of_element_located((
                    By.XPATH, 
                    '//div[@class="buy-box"]//span[contains(text(),"100% off")]')))
            free = True 
    except Exception as e:
        if isinstance(e, UdemyRobotException): raise e
        if '100% off' in browser.page_source:
            logging.exception(e)
            userWarnings.alertUser(
            "100% off in source but the check failed", 
            'Please check the CMD')
            pdb.set_trace()
            raise e
    return free

def buyCourses(urlList, userData):
    coursesBought = []
    
    browser = openBrowser()
    try:
        if not login(
            browser, 
            userData['email'], 
            userData['password']):
            return 'Login Fail'
        for url in urlList: 
            checkResult = checkCourse(browser, url) 
            if checkResult:
                buyCourse(browser)
                # logging.info(url)
                coursesBought.append(url)           
    except Exception as e:
        raise e
        logging.warning('An exception halted the execution')
        logging.warning(e)
        return 'Fail'
    finally:
        browser.close()
    return coursesBought