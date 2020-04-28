"""
 @desc:页面类的基类，封装一些常用的方法
 @author: nancy
"""
import time
import os
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException


# from public.log import Log

# log = Log()


class BasePage:
    """测试基类"""

    def __init__(self, driver):
        self.driver = driver

    @staticmethod
    def isdisplayed(element):
        """元素是否存在"""
        value = element.is_displayed()
        # if value:
        #     log.info('元素{}存在'.format(element))
        # else:
        #     log.info('元素{}不存在'.format(element))
        return value

    @staticmethod
    def my_sleep(secondes):
        """强制等待"""
        time.sleep(secondes)
        # log.info('暂停%d秒' % secondes)

    def forward(self):
        """#浏览器前进操作"""
        self.driver.forward()
        # log.info("当前页面点击前进")

    def back(self):
        """浏览器后退"""
        self.driver.back()
        # log.info("当前页面点击后退")

    def wait(self, seconds=10):
        """（整个页面）隐式等待"""
        self.driver.implicitly_wait(seconds)
        # log.info("隐式等待{}".format(seconds))

    def element_wait(self, selector, seconds=5):
        """(元素)隐式等待"""
        by = selector[0]
        value = selector[1]
        messages = '元素: {0} 没有找到 ：在{1}S内.'.format(selector, seconds)

        if by == "id":
            WebDriverWait(self.driver, seconds, 1).until(EC.presence_of_element_located((By.ID, value)), messages)
        elif by == "name":
            WebDriverWait(self.driver, seconds, 1).until(EC.presence_of_element_located((By.NAME, value)), messages)
        elif by == "class":
            WebDriverWait(self.driver, seconds, 1).until(EC.presence_of_element_located((By.CLASS_NAME, value)),
                                                         messages)
        elif by == "link_text":
            WebDriverWait(self.driver, seconds, 1).until(EC.presence_of_element_located((By.LINK_TEXT, value)),
                                                         messages)
        elif by == "xpath":
            WebDriverWait(self.driver, seconds, 1).until(EC.presence_of_element_located((By.XPATH, value)),
                                                         messages)
        elif by == "css":
            WebDriverWait(self.driver, seconds, 1).until(EC.presence_of_element_located((By.CSS_SELECTOR, value)),
                                                         messages)
        else:
            raise NameError(
                "请检查输入是否正确！!>>'id','name','class','link_text','xpaht','css'.")

    def close(self):
        """点击关闭当前窗口"""
        self.driver.close()

    def get_img(self, rq=time.strftime('%Y%m%d%H%M', time.localtime(time.time()))):
        """截图"""
        path = os.path.join(os.path.abspath('..'), 'report', 'img')
        # path = os.path.join(getcwd.get_cwd(), 'screenshots/')  # 拼接截图保存路径
        # rq = time.strftime('%Y%m%d%H%M', time.localtime(time.time()))  # 按格式获取当前时间
        screen_name = path + rq + '.png'  # 拼接截图文件名
        self.driver.get_screenshot_as_file(screen_name)

    def find_element(self, selector):
        """定位元素"""
        by = selector[0]
        value = selector[1]
        element = None
        if by in ['id', 'name', 'class', 'tag', 'link', 'plink', 'css', 'xpath']:
            # noinspection PyBroadException
            if by == 'id':
                element = self.driver.find_element_by_id(value)
            elif by == 'name':
                element = self.driver.find_element_by_name(value)
            elif by == 'class':
                element = self.driver.find_element_by_class_name(value)
            elif by == 'tag':
                element = self.driver.find_element_by_tag_name(value)
            elif by == 'link':
                element = self.driver.find_element_by_link_text(value)
            elif by == 'plink':
                element = self.driver.find_element_by_partial_link_text(value)
            elif by == 'css':
                element = self.driver.find_element_by_css_selector(value)
            elif by == 'xpath':
                element = self.driver.find_element_by_xpath(value)
            return element

    def type(self, selector, value):
        """输入内容"""
        element = self.find_element(selector)
        element.clear()
        # log.info('清空输入内容')
        # noinspection PyBroadException
        try:
            element.send_keys(value)
            # log.info('输入的内容：%s' % value)
        except BaseException as e:
            # log.error('内容输入报错{}'.format(e))
            self.get_img()

    def click(self, selector):
        """点击元素"""
        element = self.find_element(selector)
        # noinspection PyBroadException
        try:
            element.click()
            # log.info('点击元素成功')
        except BaseException as e:
            display = self.isdisplayed(element)
            if display is True:
                self.my_sleep(3)
                element.click()
                # log.info('点击元素成功')

    def right_click(self, selector):
        """右击元素"""
        # t1 = time.time()
        try:
            self.element_wait(selector)
            el = self.find_element(selector)
            ActionChains(self.driver).context_click(el).perform()
            # log.info('右击元素{}'.format(selector))
        except Exception as e:
            # log.error('右击元素{}报错,{}'.format(selector, e))
            raise

    def double_click(self, selector):
        """双击元素"""
        try:
            self.element_wait(selector)
            el = self.find_element(selector)
            ActionChains(self.driver).double_click(el).perform()
            # log.info('双击元素{}'.format(selector))
        except Exception as e:
            # log.error('双击元素{}错误'.format(selector, e))
            raise

    def get_attribute(self, selector, attribute):
        """获取元素属性值"""
        # t1 = time.time()
        try:
            # el = self.get_element(selector)
            el = self.find_element(selector)
            attr = el.get_attribute(attribute)
            # log.info('获取元素{}的属性{}值为：{}'.format(selector, attribute, attr))
            return attr
        except Exception as e:
            # log.error('获取元素{}的属性{}值错误,{}'.format(selector, attribute, e))
            raise

    def get_text(self, selector):
        """获取元素文本信息"""
        try:
            self.element_wait(selector)
            text = self.find_element(selector).text
            # log.info('获取元素{}的文本信息为：{}'.format(selector, text))
            return text
        except Exception as e:
            # log.error('获取元素{}的文本信息错误,{}'.format(selector, e))
            raise

    def use_js(self, js):
        """调用js"""

        self.driver.execute_script(js)

    def switch_menue(self, parentelement, secelement, targetelement):
        """三级菜单切换"""
        self.my_sleep(3)
        # noinspection PyBroadException
        self.driver.switch_to_default_content()
        self.click(parentelement)
        self.click(secelement)
        self.click(targetelement)

    def switch_ifarme(self, selector):
        """切换farm"""
        element = self.find_element(selector)
        # noinspection PyBroadException
        self.driver.switch_to.frame(element)

    def accept_alert(self):
        """确认报警框"""
        self.driver.switch_to.alert.accept()
        # log.info('确认报警框')

    def dismiss_alert(self):
        """确认报警框"""
        self.driver.switch_to.alert.dismiss()
        # log.info('拒绝报警框')

    def get_title(self):
        """获取title"""
        title = self.driver.title
        # log.info('当前窗口的title为{}'.format(title))
        return title

    def get_url(self):
        """获取url"""
        url = self.driver.current_url
        # log.info('当前窗口的url为{}'.format(url))
        return url

    def open(self, url):
        """打开链接"""
        # t1 = time.time()
        try:
            self.driver.get(url)
            # log.info('打开{}成功'.format(url))
            # self.my_print("{0} Navigated to {1}, Spend {2} seconds".format(success,url,time.time()-t1))
        except Exception as e:
            # log.error('打开{}成功,{}'.format(url, e))
            # self.my_print("{0} Unable to load {1}, Spend {2} seconds".format(fail, url, time.time() - t1))
            raise

    def open_new_window(self, selector):
        """在新的窗口打开链接"""
        try:
            original_windows = self.driver.current_window_handle
            el = self.find_element(selector)
            el.click()
            all_handles = self.driver.window_handles
            for handle in all_handles:
                if handle != original_windows:
                    self.driver.switch_to.window(handle)
            # log.info('点击元素{}在新窗口打开'.format(selector))
        except Exception as e:
            # log.error('点击元素{}在新窗口打开错误,{}'.format(selector, e))
            raise

    def into_new_window(self):
        """切换至新窗口"""
        # t1 = time.time()
        try:
            all_handle = self.driver.window_handles
            flag = 0
            while len(all_handle) < 2:
                time.sleep(1)
                all_handle = self.driver.window_handles
                flag += 1
                if flag == 5:
                    break
            self.driver.switch_to.window(all_handle[-1])
            # log.info('切换至新窗口，新窗口url为{}'.format(self.driver.current_url))
        except Exception as e:
            # log.error('切换至新窗口错误,{}'.format(e))
            raise

    def set_window(self, wide, high):
        """设置浏览器的宽 高"""
        # t1 = time.time()
        self.driver.set_window_size(wide, high)
        # log.info('设置浏览器宽：{} 高：{}'.format(wide, high))

    def type_Enter(self, selector):
        """输入回车"""
        try:
            el = self.find_element(selector)
            el.send_keys(Keys.ENTER)
            # log.info('输入回车')
        except Exception as e:
            # log.error('输入回车错误,{}'.format(e))
            raise

    def F5(self):
        """刷新页面"""
        # t1 = time
        self.driver.refresh()
        # log.info('刷新页面')

    def my_quit(self):
        """关闭浏览器"""
        self.driver.quit()
        # log.info('关闭浏览器')

    def original_driver(self):
        """返回原生driver"""
        return self.driver


if __name__ == '__main__':
    pass
