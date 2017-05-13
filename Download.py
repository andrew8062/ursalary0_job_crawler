from urllib import request
from bs4 import BeautifulSoup
from multiprocessing.pool import Pool
import os
import re
from Database import Db


# check the last page of this page

def get_last_page(url='http://www.ursalary0.com/salaries/salary_lists_tw/page:last'):
    with request.urlopen(url) as response:
        soup = BeautifulSoup(response.read(), 'html.parser')
        current = soup.findAll("span", class_="current")
    return int(current[0].getText())


def get_job_links(prefix, url='http://www.ursalary0.com'):
    links=set()
    with request.urlopen(url) as response:
        soup = BeautifulSoup(response.read(), 'html.parser')

    for link in soup.find_all('a'):
        links.add(link.get('href'))

    links = list(links)
    job_links = [prefix+x for x in links if 'salary_view_tw' in x and 'page' not in x]

    return job_links


def get_job_info(url):
    job_id = os.path.basename(url)
    print(job_id)
    with request.urlopen(url) as response:
        soup = BeautifulSoup(response.read(), 'html.parser')

        title = soup.find('div', {'class':'view_title_wold pull-left'}).getText()
        detail = soup.find('div', {'class':'view_content_op_review'}).getText()

        info = soup.findAll('div', {'class':'view_content_output'})
        info = [x.getText() for x in info]
        info.insert(0, title)
        info.insert(0, job_id)
        info.append(detail)

        comments = soup.findAll('div', {'class' : re.compile(r"^(reply_content_time pull-left|reply_content)$")})
        comments = [x.getText() for x in comments]
        # split all comments into sublist of time and comment, and append id in the front of each pair
        comments = [ [job_id] + comments[x:x+2] for x in range(0, len(comments), 2)]

        return info, comments


def retrieve_jobs( url):
    db = Db("jobs.db")
    job_info, comments = get_job_info(url)
    db.insert_job(job_info)
    db.insert_comment(comments)
    db.close()


def main():


    total_page = get_last_page()
    page_link = 'http://www.ursalary0.com/salaries/salary_lists_tw/page:'
    link_prefix = 'http://www.ursalary0.com/'

    for page in range(1, total_page+1):
        job_links = get_job_links(link_prefix, page_link + str(page))
        with Pool(4) as p:
            p.map(retrieve_jobs, job_links)

if __name__=='__main__':
    main()
    # get_job_info('http://www.ursalary0.com/salaries/salary_view_tw/3282')
