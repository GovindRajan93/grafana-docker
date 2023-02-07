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
options = Options()
driver = webdriver.Firefox(options=options)

print("Trying to login Azure Portal....")

def portal_login():
    driver.get('https://portal.azure.com')
    #sleep(10)
    #driver.find_element_by_xpath("//input[@id='i0116']").send_keys("govindarajan.r@soprasteria.com")
    WebDriverWait(driver, 15).until(EC.visibility_of_element_located((By.XPATH, "//input[@id='i0116']"))).send_keys("govindarajan.r@soprasteria.com")
    WebDriverWait(driver, 1).until(EC.element_to_be_clickable((By.XPATH, "//input[@id='idSIButton9']"))).click()
    WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.XPATH, "//input[@id='passwordInput']"))).send_keys("Sugan@05121995")
    WebDriverWait(driver, 1).until(EC.element_to_be_clickable((By.XPATH, "//span[@id='submitButton']"))).click()
    WebDriverWait(driver, 15).until(EC.element_to_be_clickable((By.XPATH, '//input[@id="idSIButton9"]'))).click()
    #driver.find_element_by_xpath('//input[@id="idSIButton9"]').click()
    #sleep(15)
    #driver.find_element_by_xpath("//input[@id='passwordInput']").send_keys("Sugan@05121995")
    #driver.find_element_by_xpath("//span[@id='submitButton']").click()
    #sleep(10)
    #driver.find_element_by_xpath('//input[@id="idSIButton9"]').click()
print("Logged into Azure Portal....")
portal_login()

sleep(10)
link="https://portal.azure.com/#allservices/category/All"
driver.execute_script("window.open('{}');".format(link))
driver.switch_to.window(driver.window_handles[1])
sleep(15)
driver.find_element_by_xpath('//div[@title="Shared dashboards"]').click()
driver.find_element_by_link_text("azure-learning").click()
driver.get_screenshot_as_file("/home/ansibleuser/azure-dashboards1.png")

#    driver.execute_script("window.open('{}');".format(link))
#    driver.switch_to.window(driver.window_handles[1])
#    sleep(10)
#    driver.get_screenshot_as_file(f'/opt/app/{mname}-%s.png' % now)
#    driver.close()
#    driver.switch_to.window(driver.window_handles[0])
#    driver.quit()
#    print("Dashboard alert has been captured....")
