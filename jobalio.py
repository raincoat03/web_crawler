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
    # 총 공고 개수 확인
    temp = []
    url = "https://job.alio.go.kr/recruit.do?pageNo=1"
    req = requests.get(url)
    bs = BeautifulSoup(req.content, "lxml")
    block_job = bs.select("table.tbl:nth-child(10) > tbody > tr > td")
    for i in block_job:
        temp.append(i.text)
    total_job_count = int(temp[1])

    # 변수 초기화
    page_list = [1]
    all_list= []
    add_page_list = []
    collect_job_count, n = 0, 0
    while True:
        if len(block_job) != 0:
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
                collect_job_count += 1

            page_list = [list(g) for k,g in groupby(page_list, lambda x:x =='') if not k]
            add_page_list += page_list

            # 크롤링 완료된 페이지 및 job count 확인
            print(n)
            print(collect_job_count)

            # 크롤링 내용 .csv파일로 저장
            data = pd.DataFrame(add_page_list)
            data.to_csv("jobalio.csv", encoding="utf-8-sig")

        else:
            if collect_job_count == total_job_count:
                print(total_job_count)
                print(collect_job_count)
                print("Correct")
                print(time.time() - start)
                break
            else:
                print(total_job_count)
                print(collect_job_count)
                print("Incorrect")
                print(time.time() - start)
                break

test_list = jobalio()

