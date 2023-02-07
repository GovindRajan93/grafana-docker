import sys, os, logging
import requests
import pymsteams
import time
import datetime
import slack
from time import sleep
from slack_sdk import WebClient
slack_token='xoxp-1181418301266-1187598082196-4620796761302-88c7e6294d5af8b8a5a2afa3eb5e0964'
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.keys import Keys
options = Options()
options.add_argument("--headless")
driver = webdriver.Firefox(options=options)

def portal_login():
    print("Trying to login Azure Portal....")
    driver.get('https://portal.azure.com')
    driver.fullscreen_window()
    WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.XPATH, "//input[@id='i0116']"))).send_keys("govindarajan.r@soprasteria.com")
    WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, "//input[@id='idSIButton9']"))).click()
    WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.XPATH, "//input[@id='passwordInput']"))).send_keys("Sugan@05121995")
    WebDriverWait(driver, 1).until(EC.element_to_be_clickable((By.XPATH, "//span[@id='submitButton']"))).click()
    WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, '//input[@id="idSIButton9"]'))).click()
    print("Logged into Azure Portal successfully....")
portal_login()

def dashboard_capture():
    sleep(25)
   
    from datetime import datetime
    now = datetime.now().strftime('%Y-%m-%d_%H-%M')

    link="https://portal.azure.com/#allservices/category/All"
    driver.execute_script("window.open('{}');".format(link))
    driver.switch_to.window(driver.window_handles[1])
    WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.XPATH, '//div[@title="Shared dashboards"]'))).click()
    WebDriverWait(driver, 15).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[1]/div[4]/main/div[4]/div[2]/section/div[1]/div[1]/div[4]/div[2]/div/div/div[2]/div/div[2]/div[2]/div[1]/div[3]/div/div/div[2]/div/div[2]/div[1]/div/div[1]/div[3]/div/a"))).click() 
    sleep(20)
    driver.get_screenshot_as_file(f'/home/ansibleuser/grafana-docker/azure-dashboards-%s.png' % now)
    sleep(1)
    #driver.execute_script("item=document.getElementsByClassName('scroll-body')[0];item.scrollTo(0,item.scrollHeight);")
    #driver.switch_to.frame("content-iframe")
    #driver.execute_script("window.scrollBy(0,document.body.scrollHeight);")
    #driver.find_element_by_tag_name("html").send_keys(Keys.END)
    #driver.get_screenshot_as_file(f'/home/ansibleuser/grafana-docker/azure-dashboards-scroll-%s.png' % now)
    print("Captured the dashboards....")
    driver.close()
    driver.switch_to.window(driver.window_handles[0])
    driver.quit()
    
    #Slack Notification values
    client = WebClient(token=slack_token)
    auth_test = client.auth_test()
    bot_user_id = auth_test["user_id"]

    #Slack Notification
    print("Proceeding to post the alert in slack")
    upload_file = client.files_upload(
      channels="C015BJER803",
      title=f'Azure Dashboards',
      file=f'/home/ansibleuser/grafana-docker/azure-dashboards-%s.png' % now,
      initial_comment=f'Please find the attached Azure Dashboard Report',)
    print("Dashboard Report has been posted in slack...")

    #Code to upload the reports to Azure File share

    #Create a logger for the 'azure.storage.fileshare'
    logger = logging.getLogger('azure.storage.fileshare')
    logger.setLevel(logging.DEBUG)

    #Configure a console output
    handler = logging.StreamHandler(stream=sys.stdout)
    logger.addHandler(handler)

    #Create the client
    from azure.storage.fileshare import ShareServiceClient
    service = ShareServiceClient(account_url="https://azurelearning24.file.core.windows.net/", credential="oScn4oTAR6DVyCzo5zJxX1MZJXZ+pAqawLaebD1NFI6x2HU5l7BRgyxN6DIIrtVMMH/F6B6hfukF+ASt+skywA==")
    
    #Create the Connection String
    connection_string = "DefaultEndpointsProtocol=https;AccountName=azurelearning24;AccountKey=oScn4oTAR6DVyCzo5zJxX1MZJXZ+pAqawLaebD1NFI6x2HU5l7BRgyxN6DIIrtVMMH/F6B6hfukF+ASt+skywA==;EndpointSuffix=core.windows.net"
    service = ShareServiceClient.from_connection_string(conn_str=connection_string, logging_enable=True)

    #Upload the reports file
    from azure.storage.fileshare import ShareFileClient

    file_client = ShareFileClient.from_connection_string(conn_str=connection_string, share_name="dashboardreports", file_path="azure-dashboards-%s.png" % now)

    with open("/home/ansibleuser/grafana-docker/azure-dashboards-%s.png" % now, "rb") as source_file:
         file_client.upload_file(source_file)
    print("Dashboard report has been uploaded to azure file share successfully")
dashboard_capture()
