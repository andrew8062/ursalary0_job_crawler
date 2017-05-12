from urllib import request
from bs4 import BeautifulSoup
from multiprocessing.pool import Pool
import os
import re


def get_last_page(url='http://www.ursalary0.com/salaries/salary_lists_tw/page:last'):
    with request.urlopen(url) as response:
        soup = BeautifulSoup(response.read(), 'html.parser')
        current = soup.findAll("span", class_="current")
    return int(current[0].getText())


def get_job_links(url='http://www.ursalary0.com'):
    links=set()
    with request.urlopen(url) as response:
        soup = BeautifulSoup(response.read(), 'html.parser')
    for link in soup.find_all('a'):
        links.add(link.get('href'))
    links = list(links)
    job_links = [x for x in links if 'salary_view_tw' in x and 'page' not in x]
    return job_links


def get_job_info(url):
    with request.urlopen(url) as response:
        soup = BeautifulSoup(response.read(), 'html.parser')

        title = soup.find('div', {'class':'view_title_wold pull-left'}).getText()
        detail = soup.find('div', {'class':'view_content_op_review'}).getText()

        info = soup.findAll('div', {'class':'view_content_output'})
        info = [x.getText() for x in info]
        comment = soup.findAll('div', {'class' : re.compile(r"^(reply_content_time pull-left|reply_content)$")})
        comment = [x.getText() for x in comment]
        print(comment)
        info.insert(0, title)
        info.append(detail)
        print(info)
        return info


def download_link(url):
    with request.urlopen(url) as response:
        f = open(os.path.basename(url)+'.html', 'wb')
        f.write(response.read())
        f.close()


def main():
    total_page = get_last_page()
    page_link = 'http://www.ursalary0.com/salaries/salary_lists_tw/page:'
    link_prefix = 'http://www.ursalary0.com/'

    for page in range(1, total_page+1):
        job_links = get_job_links(page_link + str(page))
        job_links = [link_prefix + x for x in job_links]

        with Pool(4) as p:
            p.map(get_job_info, job_links)

if __name__=='__main__':
    get_job_info('http://www.ursalary0.com/salaries/salary_view_tw/4312')

