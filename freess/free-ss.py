from selenium import webdriver
import logging
import json
import re
import random
import time
logging.basicConfig(level=logging.INFO)


class freess(object):
    def __init__(self):
        """
        初始化 webdriver 实例
        """
        self.url = "http://free-ss.cf"
        self.ss_data = []
        try:
            options = webdriver.ChromeOptions()
            options.add_argument("--proxy-server=127.0.0.1:8080")
            options.add_argument("headless")
            options.add_argument("--disable-gpu")
            self.chrome = webdriver.Chrome(chrome_options=options)
            logging.info("初始化 chrome(headless) ... ")
        except Exception as e:
            logging.debug(e)
            logging.error("初始化 chrome 失败 ...")
        self.get_data()

    def get_data(self):
        try:
            #调整等待参数，加快网页加载速度
            self.chrome.set_script_timeout(1)
            self.chrome.set_page_load_timeout(6)

            logging.info("正在加载 {}".format(self.url))
            self.chrome.get(self.url)
            self.chrome.implicitly_wait(3)
            time.sleep(1)
            # 找到包含信息的tr
            trs = self.chrome.find_elements_by_xpath(
                '//tr[@role="row" and @class="odd" or @class="even"] ')

            for tr in trs[4:]:
                info = tr.text
                if info != "":
                    ss = {}
                    li = info.split()
                    #过滤不安全加密方式
                    if re.search(r'cfb|gcm|chacha', li[4]):
                        li[3], li[4] = li[4], li[3]

                    ss["address"] = li[1]
                    ss["password"] = li[4]
                    ss["method"] = li[3]
                    ss["port"] = int(li[2])
                    self.ss_data.append(ss)
            logging.info("共获得{}条ss...".format(len(self.ss_data)))
            self.save_v2js()
        except Exception as e:
            logging.error(e)
            logging.error("网络异常，请稍后重试")

        finally:
            self.chrome.close()
            self.chrome.quit()

    def save_v2js(self):
        """
        随机选择部分结果 保存为v2ray_ss.json
        """
        try:
            with open('template_v2.json', 'r') as f:
                conf_v2 = json.load(f)
            d = random.sample(self.ss_data, 4)
            for ss in d:
                conf_v2['outbound']['settings']['servers'].append(ss)
            logging.info("随机写入 {}条,生成配置 v2ray_ss.json".format(
                len(conf_v2['outbound']['settings']['servers'])))
            with open('v2ray_ss.json', 'w') as f:
                json.dump(conf_v2, f, indent=4)
        except Exception as e:
            logging.error(e)


if __name__ == '__main__':
    ss = freess()
