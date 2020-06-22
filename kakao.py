import requests
from bs4 import BeautifulSoup
import lxml
import re


def kakao_job():
    url_compare = "https://careers.kakao.com/jobs?page=1&company=ALL&keyword="
    all_list = []
    r = requests.get(url_compare)
    bs = BeautifulSoup(r.content, "lxml")
    num = str(bs.find_all(attrs={"class": "link_job link_job1"}))
    number = int(re.findall("\d+", num)[-1])
    all_list_number = 0
    n = 0

    while True:
        if number > all_list_number:
            title_list, link_list = [], []
            n += 1
            url_pages = "https://careers.kakao.com/jobs?page=" + str(n) + "&company=ALL&keyword="
            r = requests.get(url_pages)
            bs = BeautifulSoup(r.content, "lxml")
            names = bs.select("a.link_notice")
            for j in names:
                link = "https://careers.kakao.com/" + j.get('href')
                job_title = j.text
                title_list.append(job_title)
                link_list.append(link)

            for k in range(len(title_list)):
                all_list.append(title_list[k] + " " + link_list[k])
            all_list_number = len(all_list)

        else:
         return all_list

all_kakao_job_list = []
all_kakao_job_list = kakao_job()
for i in all_kakao_job_list:
    print(i)