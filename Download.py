from urllib import request
from bs4 import BeautifulSoup
from multiprocessing.pool import Pool
import os


def get_job_links(url='http://www.ursalary0.com'):
    links=set()
    with request.urlopen(url) as response:
        soup = BeautifulSoup(response.read(), 'html.parser')
    for link in soup.find_all('a'):
        links.add(link.get('href'))
    links = list(links)
    job_links = [x for x in links if 'salary_view_tw' in x and 'page' not in x]
    return job_links


def download_link(url):
    with request.urlopen(url) as response:
        f = open(os.path.basename(url)+'.html', 'wb')
        f.write(response.read())
        f.close()

def main():
    total_page = 335
    page_link = 'http://www.ursalary0.com/salaries/salary_lists_tw/page:'
    link_prefix = 'http://www.ursalary0.com/'
    for page in range(1, total_page+1):
        job_links = get_job_links(page_link + str(page))
        job_links = [link_prefix + x for x in job_links]
        with Pool(4) as p:
            p.map(download_link, job_links)

if __name__=='__main__':
    main()

