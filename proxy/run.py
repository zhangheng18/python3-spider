from scrapy.utils.project import get_project_settings
from scrapy.crawler import CrawlerProcess
import os, sys


def main():
    if os.path.exists('ip.txt'):
        os.remove('ip.txt')

    setting = get_project_settings()
    process = CrawlerProcess(setting)
    didntWorkSpider = ['sample']

    for spider_name in process.spiders.list():
        if spider_name in didntWorkSpider:
            continue
        print("Running spider %s" % (spider_name))
        process.crawl(spider_name)
    process.start()


import requests
from multiprocessing.dummy import Pool as ThreadPool
pool = ThreadPool(40)

alive_ip = []


def verif_ip(proxy):
    global alive_ip
    prox = {'http': proxy}
    try:
        r = requests.get("http://www.youdao.com", proxies=prox, timeout=3)
        if 'youdao' in r.text:
            sys.stdout.write('{}......  ok !\n'.format(prox))
            alive_ip.append(proxy)

    except Exception as e:
        sys.stdout.write("{}...... fail!\n".format(prox))


def out2txt(alive_ip=[]):
    with open('ok_ip.txt', 'w') as f:
        for ip in alive_ip:
            f.write(ip + '\n')
        print("save ok!")


def test(filename='ip.txt'):
    with open(filename, 'r') as f:
        lines = f.readlines()
        proxys = list(map(lambda x: x.strip(), [y for y in lines]))
        pool.map(verif_ip, proxys)
    out2txt(alive_ip)


if __name__ == '__main__':
    main()
    test()