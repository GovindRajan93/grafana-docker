import sys, os, logging
import requests
import pymsteams
import time
import datetime
import slack
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.keys import Keys
options = Options()
driver = webdriver.Firefox(options=options)

def portal_login():
    print("Trying to login Azure Portal....")
    driver.get('https://amazon.in')
    driver.fullscreen_window()
    driver.find_element_by_tag_name("html").send_keys(Keys.END)
    print("Logged into Azure Portal successfully....")
portal_login()

def dashboard_capture():
    sleep(25)
   
    from datetime import datetime
    now = datetime.now().strftime('%Y-%m-%d_%H-%M')

    link="https://portal.azure.com/#allservices/category/All"
    driver.execute_script("window.open('{}');".format(link))
    driver.switch_to.window(driver.window_handles[1])
    WebDriverWait(driver, 25).until(EC.element_to_be_clickable((By.XPATH, '//div[@title="Shared dashboards"]'))).click()
    WebDriverWait(driver, 15).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[1]/div[4]/main/div[4]/div[2]/section/div[1]/div[1]/div[4]/div[2]/div/div/div[2]/div/div[2]/div[2]/div[1]/div[3]/div/div/div[2]/div/div[2]/div[1]/div/div[1]/div[3]/div/a"))).click() 
    sleep(10)
    driver.get_screenshot_as_file(f'/home/ansibleuser/grafana-docker/azure-dashboards-%s.png' % now)
    sleep(5)
    driver.find_element_by_tag_name("html").send_keys(Keys.END)
    driver.get_screenshot_as_file(f'/home/ansibleuser/grafana-docker/azure-dashboards-scroll-%s.png' % now)
    print("Captured the dashboards....")
    #driver.close()
    #driver.switch_to.window(driver.window_handles[0])
    #driver.quit()
#dashboard_capture()
