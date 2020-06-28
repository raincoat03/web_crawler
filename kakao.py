import requests
from bs4 import BeautifulSoup
from selenium import webdriver
import lxml
import re
import pandas as pd
import time
start = time.time()


def kakao_job():
    # 페이지 소스 가져오기
    chromedriver = "C:\\Users\\june\\Desktop\\chromedriver.exe"
    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    options.add_argument('disable-gpu')
    options.add_argument('lang=ko_KR')
    driver = webdriver.Chrome(chromedriver, options=options)
    url = "https://careers.kakao.com/jobs?page=1&company=ALL&keyword="
    driver.get(url)
    time.sleep(3)
    html = driver.page_source

    # 총 채용건수 가져오기
    page_source = BeautifulSoup(html, "lxml")
    total_count = int(page_source.find(class_="emph_num").text)
    all_list = []
    all_list_number = 0
    n = 0


    while True:
        if total_count > all_list_number:
            title_list, link_list, tag_list, hire_company_status_list = [], [], [], []
            n += 1
            url = "https://careers.kakao.com/jobs?page=" + str(n) + "&company=ALL&keyword="
            driver.get(url)
            html = driver.page_source
            page_source = BeautifulSoup(html, "lxml")
            block = page_source.findAll(class_="area_info")

            for i in block:
                job_title = str(i.find(class_="link_jobs").text)
                job_link = i.find("href")
                tag = i.findAll(class_="link_tag")
                for j in tag:
                    j = j.text
                    tag_list.append(j)
                hire_company_status = i.findAll(class_="item_subinfo")
                for k in hire_company_status:
                    k = k.text
                    hire_company_status_list.append(k)
                print(job_title)
                print(job_link)
                print(tag)
                print(hire_company_status)


            # 크롤링한 페이지 확인
            print(n)
            # 크롤링 내용 .csv파일로 저장
            data = pd.DataFrame(all_list)
            data.to_csv("kakao.csv", encoding="utf-8-sig")

        else:
         return all_list

all_kakao_job_list = []
all_kakao_job_list = kakao_job()
for i in all_kakao_job_list:
    print(i)