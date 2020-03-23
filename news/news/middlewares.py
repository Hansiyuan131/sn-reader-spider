import random
import time

import requests
from scrapy import signals
from scrapy.http.response.html import HtmlResponse
from selenium import webdriver


class UseragentDownloaderMiddleware(object):
    USER_AGENT = [
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36',
        'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML like Gecko) Chrome/44.0.2403.155 Safari/537.36',
        'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.360',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2227.1 Safari/537.36',
        'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2227.0 Safari/537.36',
        'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2227.0 Safari/537.36',
        'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2226.0 Safari/537.36'
    ]

    def process_request(self, request, spider):
        user_agent = random.choice(self.USER_AGENT)
        print(user_agent)
        request.headers['User-Agent'] = user_agent


class ProxyDownloaderMiddleware(object):
    my_proxy = [
        "223.199.26.141:18272",
        "182.84.69.21:23577",
        "119.114.238.148:20196",
        "113.138.141.98:23538",
        "116.115.210.13:22998",
    ]

    def getProxy(self):
        proxy = random.choice(self.my_proxy)
        return 'https://' + proxy

    def process_request(self, request, spider):
        print(self.getProxy())
        request.meta['proxy'] = self.getProxy()


class DownloaderMiddleware(object):

    def __init__(self):
        self.driver = webdriver.Chrome(executable_path='')

    def process_request(self, request, spider):
        self.driver.get(request.url)
        time.sleep(1)
        try:
            while True:
                showMore = self.driver.find_element_by_name('show-more')
                showMore.click()
                time.sleep(3)
                if not showMore:
                    break
        except:
            pass
        source = self.driver.page_source
        response = HtmlResponse(url=self.driver.current_url, body=source,
                                request=request, encoding='utf-8')
        return response
