from bs4 import BeautifulSoup
import requests
import re


def rocketpunchjob():
    url = "https://www.rocketpunch.com/jobs"
    req = requests.get(url)
    bs = BeautifulSoup(req.content, "html.parser")
    job_count = str(bs.find_all(attrs={"class": "active item"}))
    total_count = re.findall("\(([^)]+)", job_count)[0]
    total_count = int(total_count.replace(",", ""))
    all_list_number, n = 0, 0
    all_list = []

    while True:
        if total_count > all_list_number:
            title_list, link_list = [], []
            n += 1
            url_pages = "https://www.rocketpunch.com/jobs?page=" + str(n)
            r = requests.get(url_pages)
            bs = BeautifulSoup(r.content, "html.parser")
            names = bs.select(".company item active")
            for j in names:
                link = "https://www.rocketpunch.com/" + j.get('href')
                job_title = j.text
                title_list.append(job_title)
                link_list.append(link)

            for k in range(len(title_list)):
                all_list.append(title_list[k] + " " + link_list[k])
            all_list_number = len(all_list)

        else:
         return all_list