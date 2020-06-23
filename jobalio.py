import requests
from bs4 import BeautifulSoup
import lxml
import re
from itertools import groupby
import itertools

def jobalio():
    page_list = [1]
    all_list= []
    n = 0
    while True:
        if len(page_list) != 0:
            n += 1
            page_list = []
            url = "https://job.alio.go.kr/recruit.do?pageNo=" + str(n) + "&param=&search_yn=Y&idx=&recruitYear=&recruitMonth=&s_date=2019.11.23&e_date=2020.06.23&org_name=&ing=2&title=&order=REG_DATE"
            req = requests.get(url)
            bs = BeautifulSoup(req.content, "lxml")
            liststring = bs.select("table.tbl:nth-child(10) > tbody > tr > td")

            for i in liststring:
                a = str(i.text).rstrip()
                pattern = re.compile(r'\s+')
                a = re.sub(pattern, '', a)
                page_list.append(a)

            page_list = [list(g) for k,g in groupby(page_list, lambda x:x =='') if not k]
            all_list.append(page_list)

        else:
            all_list.pop(-1)
            return all_list

test_list = jobalio()
for i in test_list:
    for j in i:
        print(j)