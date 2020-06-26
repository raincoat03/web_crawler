'''
'''
from bs4 import BeautifulSoup
from selenium import webdriver
from itertools import groupby
import requests
import re
import time
import lxml
import pandas as pd
import numpy as np
start = time.time()


# 총 채용공고 숫자 검색(bs4)
url = "https://www.rocketpunch.com/jobs?page=1"
req = requests.get(url)
bs = BeautifulSoup(req.content, "lxml")
job_count = str(bs.find_all(attrs={"class": "active item"}))
total_count = re.findall("\(([^)]+)", job_count)[0]
total_count = int(total_count.replace(",", ""))

# selenium으로 첫번째 페이지 가져오기
chromedriver = "C:\\Users\\june\\Desktop\\chromedriver.exe"
options = webdriver.ChromeOptions()
options.add_argument('headless')
options.add_argument('disable-gpu')
options.add_argument('lang=ko_KR')
driver = webdriver.Chrome(chromedriver, options = options)
driver.get(url)
time.sleep(3)
html = driver.page_source
page = BeautifulSoup(html, 'lxml')

# 한 페이지 내의 회사 개수 파악
companylist = page.find(class_= "ui job items segment", id = "company-list")
company_title = companylist.findAll(class_="header name")
content_total = []
n = 0
content_count = 0

while True:
    n += 1
    url = "https://www.rocketpunch.com/jobs?page=" + str(n)
    driver.get(url)
    time.sleep(3)
    html = driver.page_source
    page = BeautifulSoup(html, 'lxml')
    companylist = page.find(class_="ui job items segment", id="company-list")
    company_title = companylist.findAll(class_="header name")

    if len(company_title) != 0:
        # content active 블록에서 필요한 정보 추출
        '''
        content_active = []
        ## 회사명/링크 추출 및 리스트에 추가
        block_active = companylist.find(class_= "content active")
        block_active_name = block_active.findAll(class_= "header name")
        block_active_link = block_active.find("a", href = True)
        block_active_link = block_active_link["href"]
        company_link = "https://www.rocketpunch.com" + block_active_link
        
        for name in block_active_name:
            name = str(name.text.strip())
            pattern = re.compile(r'\s+')
            name = re.sub(pattern, '', name)
            namewithlink = name + " " + ":" + " " + company_link
            content_active.append(namewithlink)
        
        ## 직무명/링크 추출 및 리스트에 추가
        block_active_job = block_active.findAll(class_= "nowrap job-title primary link")
        for i in block_active_job:
            job_title = i.text
            job_link = "https://www.rocketpunch.com" + i.get("href")
            job_total = job_title + " " + ":" + " " + job_link
            content_active.append(job_total)
        content_total.append(content_active)
        '''

        # content 태그 회사 추출
        block = companylist.findAll(class_= "content")

        ## 회사명/링크 추출 및 리스트에 추가
        for i in range(len(block)):
            temp, temp2 = [], []
            content = []
            block_name = block[i].findAll(class_="header name")
            block_link = block[i].find("a", href=True)
            if block_link != "/signup":
                block_link = block_link["href"]
            company_link = ("https://www.rocketpunch.com" + block_link).strip()
            for name in block_name:
                name = str(name.text.strip())
                pattern = re.compile(r'\s+')
                name = re.sub(pattern, '', name)
                namewithlink = (name + "(" + company_link + ")").strip()
                content.append(namewithlink)

        ## 직무명/링크 추출 & 리스트에 추가
            block_job = block[i].findAll(class_="nowrap job-title primary link")
            for i in block_job:
                job_title = i.text
                job_link = "https://www.rocketpunch.com" + i.get("href")
                job_total = (job_title + "(" + job_link + ")").strip()
                content_count += 1
                content.append(job_total)
            content_total.append(content)

        ## 크롤링 완료된 페이지 확인
        print(n)

        ## 크롤링 내용 .csv파일로 저장
        data = pd.DataFrame(content_total)
        data.to_csv("rocketpunch.csv", encoding = "utf-8-sig")

    else:
        break

if content_count == total_count:
    print(content_count)
    print(total_count)
    print("Correct")
    print(time.time()-start)
else:
    print(content_count)
    print(total_count)
    print("Incorrect")
    print(time.time()-start)