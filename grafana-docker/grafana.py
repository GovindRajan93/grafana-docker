import sys, os, logging
import requests
import time
import datetime
import slack
from time import sleep
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
options = Options()
options.binary_location = r'/opt/app-root/bin/firefox/firefox'
options.add_argument("--headless")
driver = webdriver.Firefox(executable_path=r'/opt/app-root/bin/geckodriver', options=options)
driver = webdriver.Firefox(options=options)
from slack_sdk import WebClient
slack_token=''
client = WebClient(token=slack_token)
auth_test = client.auth_test()
bot_user_id = auth_test["user_id"]

def grafana_login():
    driver.get('http://localhost:3000/login')
    sleep(10)
    driver.find_element_by_xpath('//*[@name ="user"]').send_keys("admin")
    driver.find_element_by_xpath('//*[@name="password"]').send_keys("admin123")
    login=driver.find_element_by_xpath("//span[text()='Log in']")
    login.click()

def capture_alert(pid, mname):
    import datetime
    import time
    current_time = datetime.datetime.now()
    five_min_ago = current_time - datetime.timedelta(minutes=5)
    from_ts = int(five_min_ago.timestamp() * 1000)
    to_ts = int(time.time() * 1000)
    link=f'http://localhost:3000/d/rYdddlPWk/node-exporter-full?orgId=1&from={from_ts}&to={to_ts}&viewPanel={pid}'

    from datetime import datetime
    now = datetime.now().strftime('%Y-%m-%d_%H-%M')

    driver.execute_script("window.open('{}');".format(link))
    driver.switch_to.window(driver.window_handles[1])
    sleep(10)
    driver.get_screenshot_as_file(f'/opt/app/{mname}-%s.png' % now)
    driver.close()
    driver.switch_to.window(driver.window_handles[0])
    driver.quit()

    upload_file = client.files_upload(
      channels="C015BJER803",
      title=f'Alert: {mname}',
      file=f'/opt/app/{mname}-%s.png' % now,
      initial_comment=f'Kindly check the below stats in {mname}\n' f'Grafana URL: {link}',)

def metric_name():
    if len(sys.argv) > 1:
       if sys.argv[1] == "1":
          grafana_login()
          capture_alert(77, "CPU")
       elif sys.argv[1] == "2":
          grafana_login() 
          capture_alert(78, "Memory")
       elif sys.argv[1] == "3":
          grafana_login()
          capture_alert(74, "Network")
       elif sys.argv[1] == "4":
          grafana_login()
          capture_alert(152, "Disk Space")
    elif len(sys.argv) == 1:
       print("Please pass appropriate value to process")

metric_name()
