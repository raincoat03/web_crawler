import requests
from bs4 import BeautifulSoup
import lxml
import re
from itertools import groupby
import itertools
import pandas as pd
import time
start = time.time()

def jobalio():
    page_list = [1]
    all_list= []
    add_page_list = []
    n = 0
    while True:
        if len(page_list) != 0:
            n += 1
            page_list = []
            url = "https://job.alio.go.kr/recruit.do?pageNo=" + str(n)
            req = requests.get(url)
            bs = BeautifulSoup(req.content, "lxml")
            block_job = bs.select("table.tbl:nth-child(10) > tbody > tr > td")

            for i in block_job:
                job_description = str(i.text).rstrip()
                pattern = re.compile(r'\s+')
                job_description = re.sub(pattern, '', job_description)
                page_list.append(job_description)

            page_list = [list(g) for k,g in groupby(page_list, lambda x:x =='') if not k]
            add_page_list += page_list
            ## 크롤링 완료된 페이지 확인
            print(n)

            ## 크롤링 내용 .csv파일로 저장

            data = pd.DataFrame(add_page_list)
            data.to_csv("jobalio.csv", encoding="utf-8-sig")


        else:
            return add_page_list

test_list = jobalio()
print(time.time()-start)