# -*- coding: utf-8 -*-
"""
Created on Tue Feb 28 14:23:00 2017

@author: icaromarley5

Wrap-up for selenium functions
"""

from selenium import webdriver
import time
import sys
sys.path.append('../tools/')
import threads

chrome_path = '../drivers/chromedriver'

browser_list = [] 
max_count = 4
count = 0  
finalized = False  
watch_dog = None
check_interval = 1 * 60 * 0.5 # 30 seconds

def create(limit=5):  # 5 h
    global count
    count += 1
    driver = webdriver.Chrome(chrome_path)
    driver.start_time = time.time()
    driver.time_limit = limit
    driver.released = False

    browser_list.append(driver)

    return driver

def release(browser):
    browser.released = True
    return True

# ends all executions 
def finalize():
    global finalized, watch_dog
    finalized = True
    watch_dog.join()
    watch_dog = None

# initialize the variables 
# call watch function
def initialize():
    global finalized, watch_dog
    finalized = False

    if watch_dog != None:
        finalize()
    args = {}
    thread = threads.TaskThread(watch, args)
    thread.start()
    watch_dog = thread

# watch the browsers
def watch():
    global count, browser_list, finalized, check_interval

    while (True):
        i = 0
        while i < len(browser_list):
            browser = browser_list[i]
            now = time.time()
            execution_time = (now - browser.start_time) / (60 * 60)
            if (browser.released) or execution_time > \
                browser.time_limit or finalized:
                
                print("Killing browser",
                    i,execution_time,browser.released)
                browser_list.pop(i)
                browser.quit()
                count += -1
                i += -1
            i += 1

        if finalized:
            break
        #print(len(browser_list))
        time.sleep(check_interval)

def get_count_browsers():
    global count
    return count

def get_max_browsers():
    global max_count
    return max_count

def at_max_count():
    global count, max_count
    return count >= max_count

# creates processing threads based on max number of active browsers
# task inputs are a list and a browser
# task returns a list
def process_task(task, input_list):
    n_input = len(input_list)
    
    # creates browsers
    browser_list = []
    if input_list:  # if not empty
        while not browser_list:  # while no browser is created
            #print("max",at_max_count())
            while not at_max_count() and len(browser_list) < n_input:
                # creates until hits the max number allowed
                # and number of browsers < len(list)
                browser_list.append(create())
    else:  # only one browser
        browser_list.append(create())
    thread_list = []

    n_browser = len(browser_list)
    separator = n_input // n_browser  # separador da lista
    mod = n_input % n_browser

    # split output and throw task threads for each split
    base = 0
    for index, browser in enumerate(browser_list):
        floor = base
        top = base + separator
        if (index == n_browser - 1):  # last browser
            top += mod  # get whats left of the input
        args = {"input_list": input_list[floor: top], "browser": browser}
        thread = threads.TaskThread(task, args)
        # starts thread
        thread.start()
        thread_list.append(thread)
        base += separator

    results = []
    for t in thread_list:
        results += t.join()

    # kill all browsers created
    for browser in browser_list:
        release(browser)

    return results

def process_multi_tasks(functions,input_list):
    initialize()

    thread_list = []
    args = {"input_list":input_list}
    for function in functions:  
        args["task"] = function
        thread = threads.TaskThread(process_task, args)
        #starts thread
        thread.start()
        thread_list.append(thread)
       
    # collect results
    results = []
    for t in thread_list:
        results+=t.join()
  
    finalize()
    
    return results