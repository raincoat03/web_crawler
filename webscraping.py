from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time
import pandas as pd
import re
from bs4 import BeautifulSoup
import requests
import re


'''
chromedriver = "C:\\Users\\june\\Desktop\\chromedriver.exe"
url = "https://www.rocketpunch.com/jobs?page=1"
options = webdriver.ChromeOptions()
options.add_argument('headless')
options.add_argument('disable-gpu')
options.add_argument('lang=ko_KR')
driver = webdriver.Chrome(chromedriver)
driver.get(url)
time.sleep(5)                                                   # selenium을 통해 rocketpunch 채용 첫 페이지 접근
'''

url = "https://www.rocketpunch.com/jobs"
req = requests.get(url)
bs = BeautifulSoup(req.content, "html.parser")
job_count = str(bs.find_all(attrs={"class": "active item"}))
total_count = re.findall("\(([^)]+)", job_count)[0]
total_count = int(total_count.replace(",", ""))                 # bs4 이용해 job 개수 구함


all_page = bs.find("div", {"id":"company-list"}).findAll("strong")
print(all_page)
