"""
 @desc:选择浏览器
 @author: nancy
"""
import os
import sys
from selenium import webdriver
# from public.log import Log
from public.readconfig import ReadConfig

# log = Log()
chrome_driver = os.path.join(os.path.dirname(os.path.abspath(sys.argv[0])), 'webdriver', 'chromedriver.exe')
firefox_driver = os.path.join(os.path.dirname(os.path.abspath(sys.argv[0])), 'webdriver', 'geckodriver.exe')


class BrowserEngine(object):

    def __init__(self, driver):
        self.driver = driver

    def open_browser(self, driver):
        read = ReadConfig()
        browser = read.getValue("browserType", "browserName")
        options = read.getValue("pattern", "options")
        url = read.getValue("testServer", "URL")
        is_visible = read.getValue("pattern", "is_visible")

        if options.lower() == 'web':
            if browser == "Firefox":
                # if is_visible == 'F':
                #     options = webdriver.FirefoxOptions()
                #     #options.add_argument('-headless')
                #     # options.add_argument('--disable-gpu')
                #     driver = webdriver.Firefox(executable_path=firefox_driver, options=options)
                # else:
                #     driver = webdriver.Firefox(executable_path=firefox_driver)
                #     log.info("启动{}浏览器".format(browser))
                driver = webdriver.Firefox()

            elif browser == "Chrome":
                if is_visible == 'F':
                    option = webdriver.ChromeOptions()
                    option.add_argument('headless')
                    driver = webdriver.Chrome(chrome_driver, chrome_options=option)
                else:
                    driver = webdriver.Chrome(chrome_driver)
                    # log.info("启动{}浏览器".format(browser))

            # elif browser == "IE":
            #     driver = webdriver.Ie(driver_path)
            #     log.info("启动{}浏览器".format(browser))
        elif options.lower() == 'wap':
            mobileEmulation = {"deviceName": "iPhone 6"}
            options = webdriver.ChromeOptions()
            options.add_experimental_option('mobileEmulation', mobileEmulation)
            options.add_argument('--disable-search-geolocation-disclosure')
            driver = webdriver.Chrome(chrome_options=options)

        driver.get(url)
        # log.info("打开链接：{}".format(url))
        # driver.maximize_window()
        # log.info("最大化窗口")
        # driver.implicitly_wait(10)
        # log.info("隐式等待10s")
        return driver

    def quit_browser(self):
        # log.info("退出浏览器驱动")
        self.driver.quit()


if __name__ == '__main__':
    print(os.path.join(os.path.abspath('..'), 'config', 'config.ini'))
