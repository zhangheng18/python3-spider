# Python3 爬虫项目实战
* 爬虫实战：不是单纯的演示，功能完整可用。
* [个人网站](https://xiaotaoist.github.io)

## 声明
代码且仅限于学习交流

## 目录
* [E小说下载器](https://github.com/xiaoTaoist/python3-spider/blob/master/seek_books.py)
* [scrapy-proxy](https://github.com/xiaoTaoist/python3-spider/tree/master/proxy)


## 介绍
* seek_books.py: E小说 盗版小说网站，多线程下载小说工具
    * 第三方依赖：
        > pip install requests beautifulsoup4
    * 演示：
        ![seek_books](https://raw.githubusercontent.com/xiaoTaoist/python3-spider/master/demo_pic/seek_books.png)
    
* proxy:使用scrapy框架，对网上免费代理进行收集,验证，提取可用的http 代理
    * 第三方依赖：
        > pip install requests scrapy
    * 爬取的网站:
        * http://www.data5u.com
        * http://lab.crossincode.com
        * https://www.kuaidaili.com/
        * http://spys.me/proxy.txt
        * http://www.xicidaili.com/
    * 使用: 抓取列表保存为ip.txt, 可用代理保存在ok_ip.txt
        > python run.py

