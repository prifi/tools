#!usr/bin/env python
# -*- coding:utf-8 _*-
"""
@version:
author:fly
@time: 2022/06/07
@file: selenium绕过webdriver检测.py
"""
from selenium import webdriver

class WebDriverChrome(object):
    """测试绕过webdriver的检测属性"""
    def __init__(self):
        self.driver = self.StartWebdriver()

    def StartWebdriver(self):
        options = webdriver.ChromeOptions()
        options.add_argument("start-maximized")
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option("useAutomationExtension", False)
        driver = webdriver.Chrome(options=options)
        # window.navigator.webdriver ==> false
        with open('./stealth.min.js') as f:
            js = f.read()
        driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
            "source": js
        })
        return driver

    def RunStart(self):
        self.driver.get('https://bot.sannysoft.com')
        # time.sleep(10)
        # self.driver.quit()


if __name__ == '__main__':
    Crawl = WebDriverChrome()
    Crawl.RunStart()