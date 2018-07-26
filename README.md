# Python3 爬虫项目实战
* 爬虫实战：不是单纯的演示，功能完整可用。
* [个人网站](https://xiaotaoist.github.io)

## 声明
代码且仅限于学习交流

## 目录
* [E小说下载器](https://github.com/xiaoTaoist/python3-spider/blob/master/seek_books.py)
* [scrapy-proxy](https://github.com/xiaoTaoist/python3-spider/tree/master/proxy)
* [selenium-freess](https://github.com/xiaoTaoist/python3-spider/tree/master/freess)


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



* freess:使用Chrome(headless)对[free-ss](https://free-ss.site)进行访问，抓取里面可用信息，保存为[v2ray](https://github.com/v2ray/v2ray-core/releases) 配置文件。
    * 第三方依赖：
        > pip install selenium  mitmproxy bs4 lxml
    * 使用：
        * 安装最新版[Chrome浏览器](https://api.shuax.com/tools/getchrome) 和 [chromedriver](http://npm.taobao.org/mirrors/chromedriver) (Windows用户需要将下载好的`chromedriver.exe`放到当前目录)
        * 使用mimtproxy对网页注入js全局变量，以绕过对webdriver的检测机制
            > mitmdump -s inject.py --ignore-host "cdn.jsdelivr.net:443"
        * 演示:  
            ![seek_books](https://raw.githubusercontent.com/xiaoTaoist/python3-spider/master/demo_pic/free-ss.png)
        




