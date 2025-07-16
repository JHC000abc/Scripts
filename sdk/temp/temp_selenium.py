#!/usr/bin/python3
# -*- coding:utf-8 -*-
"""
@author: JHC
@file: temp_selenium.py
@time: 2023/6/23 20:39
@desc:
"""
import random
import time
# selenium 不支持捕获接口
from selenium import webdriver
# seleniumwire 支持捕获接口
from seleniumwire import webdriver
from webdriver_manager.chrome import ChromeDriverManager
# from webdriver_manager.microsoft import EdgeChromiumDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from lxml import etree
import sys


SLIDING_DISTANCE = 500


class BaseSelenium(object):
    """
    Selenium 基类
    """

    def __init__(self, headless=False, headers=None, proxy=None,
                 cookies=None, dev=False, incognito=False, debug_port=None, timeout=100, chrome_path=None):
        """

        :param headless:是否无头模式
        :param headers:
        :param proxy:
        :param cookies:
        :param dev:是否开启开发者模式
        :param incognito:是否开启无痕模式
        :param timeout:等待超时时间
        """
        super(BaseSelenium, self).__init__()
        self.chrome_path = chrome_path
        self.chrome_options = None
        self.driver = None
        self.temp_height = 0
        self.timeout = timeout
        self.tree = None
        self.history = {}
        self.headless = headless
        self.headers = headers
        self.cookies = cookies
        # proxy=127.0.0.1:8080
        self.proxy = proxy
        self.dev = dev
        # 无痕模式
        self.incognito = incognito
        # 浏览器接管监听端口 9527  chrome.exe --proxy-server=127.0.0.1:7890 --remote-debugging-port=9527 --user-data-dir= Application\userdata
        # chrome浏览器默认user data 地址：C:\Users\JHC00\AppData\Local\Google\Chrome\User Data 里边数据直接放到user-data-dir里就行了
        # 存在 debug_port 即为接管模式
        # 接管模式下钩子抓不到接口数据（暂未解决）
        self.debug_port = debug_port
        self.load_options()

    def _init_tree(self):
        """
        初始化xpath
        :return:
        """
        if not self.tree:
            page_source = self.get_page_source()
            tree = etree.HTML(page_source)
            self.tree = tree
        return self.tree

    def load_options(self):
        """
        加载排至参数
        :return:
        """
        chrome_options = Options()
        if self.incognito:
            chrome_options.add_argument('--incognito')
        if self.debug_port:
            chrome_options.add_experimental_option(
                "debuggerAddress", "127.0.0.1:{}".format(self.debug_port))
        else:
            if self.headless:
                chrome_options.add_argument('--headless')  # 可视化界面
            if self.proxy:
                chrome_options.add_argument(
                    '--proxy-server={}'.format(self.proxy))
            if self.headers:
                chrome_options.add_argument(
                    'user-agent={}'.format(self.headers))
            if self.dev:
                chrome_options.add_argument("--auto-open-devtools-for-tabs")
            chrome_options.add_experimental_option('detach', True)  # 不自动关闭浏览器
            chrome_options.add_experimental_option(
                'useAutomationExtension', False)
            chrome_options.add_experimental_option(
                "excludeSwitches", ['enable-automation'])

        chrome_options.add_argument('--start-maximized')  # 浏览器窗口最大化
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--ignore-certificate-errors')
        chrome_options.add_argument(
            '--disable-blink-features=AutomationControlled')
        chrome_options.add_argument("disable-blink-features")
        chrome_options.add_argument('--ignore-urlfetcher-cert-requests')

        self.chrome_options = chrome_options

    def get_driver(self):
        """
        获取driver
        :return:
        """
        if not self.chrome_options:
            self.load_options()

        if not self.driver:
            if self.chrome_path:
                driver = webdriver.Chrome(executable_path=self.chrome_path, options=self.chrome_options)
            else:
                service = Service(ChromeDriverManager().install())
                driver = webdriver.Chrome(
                    service=service, options=self.chrome_options)

            self.driver = driver
        return self.driver

    def rolldown(self, sleep=1, repeat=3):
        """
        下滑到网页底部
        :param driver:
        :return:
        """
        driver = self.get_driver()
        driver.execute_script("window.scrollBy(0,{})".format(SLIDING_DISTANCE))
        time.sleep(0.1)
        check_height = driver.execute_script(
            "return document.documentElement.scrollTop "
            "|| window.pageYOffset "
            "|| document.body.scrollTop;"
        )
        while check_height != self.temp_height:
            self.temp_height = check_height
            if self.history.get(check_height) is not None:
                if self.history[check_height] > repeat:
                    break
                else:
                    self.history[check_height] = self.history[check_height] + 1
                    time.sleep(sleep)
            else:
                self.history[check_height] = 0
                time.sleep(sleep)
                self.rolldown()

    def get_page_source(self):
        """
        获取源码
        :return:
        """
        driver = self.get_driver()
        return driver.page_source

    def close_chrome(self):
        """
        关闭浏览器
        :return:
        """
        driver = self.get_driver()
        try:
            driver.close()
            driver.quit()
        except BaseException:
            sys.exit(0)
        # finally:
        #     sys.exit(0)

    def wait_load_finish(self, label):
        """
        通过判断页面元素是否存在 决定是否继续等待页面加载
        :param label:
        :return:
        """
        driver = self.get_driver()
        flag = False
        try:
            WebDriverWait(driver, self.timeout).until(
                EC.presence_of_element_located((By.XPATH, label))
            )
            flag = True
        except BaseException:
            print("Wait Timeout {}".format(self.timeout))
        finally:
            return flag

    def login(self):
        """
        加载cookies登录
        :param self.cookies:{'name':'ABC','value':'DEF'}
        :return:
        """
        driver = self.get_driver()
        driver.delete_all_cookies()
        for k, v in self.cookies.items():
            driver.add_cookie({"name": k, "value": v})
        driver.refresh()

    def load_url(self, url):
        """

        :param url:
        :return:
        """
        driver = self.get_driver()
        driver.get(url)
        if self.cookies:
            self.login()
            print("Login Success !!!")

    def hock_data_by_urls(self, url_list):
        """
        下钩子通过判断url捕获请求返回数据
        :param url_list:url唯一标识列表
        :return:
        """
        driver = self.get_driver()
        for request_method in driver.requests:
            url = request_method.url
            for args in url_list:
                if args in url:
                    response = request_method.response.body
                    yield {
                        "args": args,
                        "url": url,
                        "response": response,
                    }

    def control_silder(self, element, distance, iframe_name=None, offset=10):
        """

        :param element:
        :param distance:
        :return:
        """
        self.get_driver()
        # 切换iframe
        if iframe_name:
            self.driver.switch_to.frame(
                self.driver.find_element(by=By.XPATH, value='//html//body//iframe//{}'.format(iframe_name)))
        source = self.driver.find_element(
            by=By.XPATH, value='{}'.format(element))
        # 虚拟轨迹
        ActionChains(self.driver).click_and_hold(source).perform()
        off = random.randint(0, 9)
        move_lis = [distance + offset + off, -off]
        for opt in move_lis:
            ActionChains(self.driver).move_by_offset(opt, 0).perform()
            time.sleep(float("0.{}".format(random.randint(1, 9))))
        # 直接到真实坐标
        # ActionChains(self.driver).move_by_offset(distance+offset, 0).perform()
        time.sleep(0.1)
        ActionChains(self.driver).release().perform()

    def main(self, url):
        """

        :param url:
        :return:
        """
        self.history.clear()
        self.load_url(url)
        self.rolldown()
        # if self.wait_load_finish('//div[@class="gWel-mailInfo-txt"]'):
        for result in self.hock_data_by_urls(["article/details/131357346"]):
            print(result["url"])

            # print(driver.get_cookies())
            # print(self.get_page_source())
            # res = driver.find_element(by=By.XPATH, value="//code[@class='prism language-python has-numbering']")
            # print(res.text)

        self.close_chrome()


if __name__ == '__main__':
    url = 'https://twitter.com/search?q=time%20loopgame&src=recent_search_click'
    while True:
        BaseSelenium(debug_port=9528).main(url)
