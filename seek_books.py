"""
从E小说 https://www.zwda.com/ 搜索小说，并保存为txt，支持多线程。
re,requests,BeautifulSoup

"""

import argparse
import sys

import queue
import threading

import re
import requests
from urllib.parse import quote
from bs4 import BeautifulSoup as BS

from colorama import Back, Fore, init
init(autoreset=True)

book_text = {}


class E_books(object):
    def __init__(self, name, threads_num):
        self._head = {
            "User-Agent":
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.2704.103 Safari/537.36"
        }
        self._name = name
        self._threads = threads_num
        self._que = queue.Queue()
        self._book_list = {}
        self._book_url = None
        self._total = 0

    def get_html(self, url):
        try:
            r = requests.get(url, headers=self._head)
            r.raise_for_status()
            return r.content
        except:
            raise "网络错误"

    def get_book_info(self):
        url = "https://www.zwda.com/search.php?keyword=" + quote(self._name)
        html = self.get_html(url)
        soup = BS(html, 'lxml')
        liTags = soup.find_all('div', class_='result-item result-game-item')
        id = 0
        for li in liTags:
            self._book_list[id] = {}
            comment = self._book_list[id]
            try:
                comment['name'] = li.find(
                    'a', class_='result-game-item-title-link')['title']
                comment['link'] = li.find(
                    'a', class_='result-game-item-title-link')['href']
                comment['author'] = li.find_all(
                    'span', class_="")[1].text.strip()
                comment['info'] = li.find(
                    'p', class_='result-game-item-desc').text.strip()
                comment['newchapter'] = li.find(
                    'a', class_='result-game-item-info-tag-item').text.strip()

                id += 1

            except:
                raise "获取内容错误!"
        self.output()

    def output(self):
        col = Colored()
        # import ipdb
        # ipdb.set_trace()
        if self._book_list == {}:
            pprint("暂未找到{}".format(self._name))
            raise "该书暂未收录"
        else:
            book_ids = len(self._book_list) - 1

            for i in self._book_list:
                info = self._book_list[i]
                pprint('{}. 《{}》 {} \t{}\n\t{}\n'.format(
                    col.white_yellow(str(i)),
                    col.green(info['name']), info['author'],
                    col.yellow("最新章节：" + info['newchapter']), info['info']))
            if not book_ids == 0:
                book_ids = int(input("要下载的编号："))
            try:
                self._book_url = self._book_list[book_ids]['link']
                self._name = self._book_list[book_ids]['name']
            except:
                raise "编号错误!"
            self.get_chapter_urls()

    def get_chapter_urls(self):
        html = self.get_html(self._book_url)

        soup = BS(html.decode('gbk'), 'html.parser')
        lis = soup.find(id='list').find_all('a')
        for i in lis:
            self._que.put("https://www.zwda.com" + i['href'])

        self._total = len(lis)
        pprint("共需要下载{}章".format(self._total))

    def download(self):
        while not self._que.empty():
            url = self._que.get()
            html = self.get_html(url)
            soup = BS(html.decode('gbk'), 'html.parser')
            content = soup.find(id='content').text.replace(
                '\xa0\xa0\xa0\xa0', '\n  ')
            chapter = soup.find('h1').text

            id = Cn2An(get_tit_num(chapter))

            sys.stdout.write("已下载:%.2f%%" %
                             (100 - self._que.qsize() / self._total * 100) +
                             '\r')
            sys.stdout.flush()

            book_text[id] = {}
            text = book_text[id]
            text['title'] = chapter
            text['text'] = content

    def save2txt(self):

        file = self._name + '.txt'
        with open(file, 'w') as f:
            for i in range(len(book_text)):
                try:
                    # import ipdb
                    # ipdb.set_trace()
                    text = book_text[i]

                    f.write("{}\n{}\n\n".format(text['title'], text['text']))
                except:
                    pprint("第{}章获取 错误!".format(i))

        pprint("{} 下载成功!".format(file))

    def run(self):
        self.get_book_info()

        threads = []
        for i in range(self._threads):
            threads.append(threading.Thread(target=self.download))

        for i in threads:
            i.start()
        for i in threads:
            i.join()

        self.save2txt()


def pprint(s):
    sys.stdout.write("{}\n".format(s))


#更美观的显示效果
class Colored(object):
    def red(self, s):
        return Fore.RED + s + Fore.RESET

    def green(self, s):
        return Fore.GREEN + s + Fore.RESET

    def yellow(self, s):
        return Fore.YELLOW + s + Fore.RESET

    def white_yellow(self, s):
        return Fore.WHITE + Back.YELLOW + s + Fore.RESET + Back.RESET


num = re.compile(r"[第]?(.*?)章")


def get_tit_num(title):
    tit = title.split(' ')
    result = ""
    if len(tit) == 2:
        num_list = [
            '1', '2', '3', '4', '5', '6', '7', '8', '9', '0', '一', '二', '两',
            '三', '四', '五', '六', '七', '八', '九', '十', '零', '〇', '千', '百'
        ]
        for char in tit[0]:
            if char in num_list:
                result += char
    else:
        try:
            result = num.findall(title)[0]
        except:
            result = '0'

    return result


#汉字转数字，方便排序
def Cn2An(chinese_digits):

    chs_arabic_map = {
        '零': 0,
        '一': 1,
        '二': 2,
        '两': 2,
        '三': 3,
        '四': 4,
        '五': 5,
        '六': 6,
        '七': 7,
        '八': 8,
        '九': 9,
        '十': 10,
        '百': 100,
        '千': 10**3,
        '〇': 0,
        '0': 0,
        '1': 1,
        '2': 2,
        '3': 3,
        '4': 4,
        '5': 5,
        '6': 6,
        '7': 7,
        '8': 8,
        '9': 9
    }

    result = 0
    tmp = 0
    hnd_mln = 0
    for count in range(len(chinese_digits)):
        curr_char = chinese_digits[count]
        curr_digit = chs_arabic_map[curr_char]
        # meet 「十」, 「百」, 「千」 or their traditional version
        if curr_digit >= 10:
            tmp = 1 if tmp == 0 else tmp
            result = result + curr_digit * tmp
            tmp = 0
        # meet single digit
        elif curr_digit is not None:
            tmp = tmp * 10 + curr_digit
        else:
            return result
    result = result + tmp
    result = result + hnd_mln
    return result


def main(agrs):
    name = args.keys
    if name == None:
        name = input("请输入小说名：")

    book = E_books(name, args.threads)
    book.run()


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description="E小说 下载器 ")
    parser.add_argument("-k", "--keys", help="要搜索的书名")
    parser.add_argument("-t", "--threads", type=int, default=20, help="指定线程数")
    args = parser.parse_args()

    main(args)
