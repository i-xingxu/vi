# coding=utf-8
from ..common import conf
from ..common import tool
from ..common import logoutput
import time
import os
from selenium.webdriver.support.ui import WebDriverWait
from selenium import webdriver
import allure
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium.webdriver import Chrome
from selenium.webdriver import ChromeOptions
from selenium.webdriver.common.action_chains import ActionChains


class SetUp():
    '''
    appbase中setup类，用来启动app，返回一个driver对象
    '''

    def __init__(self):
        # self.CONF_PATH = CONF_PATH
        self.lg = logoutput.Logger()
        self.cf = conf.Conf()

    def web_setup(self, chromenum=1):
        '''

        :param chromenum: 使用多线程并行启动chrome时需要使用多个User Data文件夹，默认为1，即只使用一个User Data文件夹；为2时，需要在User Data文件夹同级目录复制一份，取名为User Data - 1
        :return:
        '''

        try:
            CONF_BRO_CONF = "BrowserConfig"
            CONF_FIR_PATH_NAME = "firefoxpath"
            CONF_FIR_PROFILE = "firefoxprofile"
            CONF_BROWSER = "Browser"
            CONF_BRO_TYPE = "browser"
            CONF_CHRO_PATH_NAME = "chromprofile"
            CONF_CHRO_ISDISPLAY = "chromeisdisplay"
            CONF_CHRO_PROXY = 'ChromeProxy'
            CONF_CHRO_PROXY_TYPE = 'type'
            CONF_CHRO_PROXY_INFO = 'proxy'

            browserType = self.cf.get_conf_data(CONF_BROWSER)[CONF_BRO_TYPE]
            if browserType == "Firefox":
                binary = FirefoxBinary(self.cf.get_conf_data(CONF_BRO_CONF)[CONF_FIR_PATH_NAME])
                fp = webdriver.FirefoxProfile(self.cf.get_conf_data(CONF_BRO_CONF)[CONF_FIR_PROFILE])
                driver = webdriver.Firefox(firefox_binary=binary, firefox_profile=fp)
                return driver
            elif browserType == "Chrome":

                option = ChromeOptions()
                proxyType = self.cf.get_conf_data(CONF_CHRO_PROXY)[CONF_CHRO_PROXY_TYPE]
                proxyInfo = self.cf.get_conf_data(CONF_CHRO_PROXY)[CONF_CHRO_PROXY_INFO]
                if int(proxyType) == 1:
                    option.add_argument(proxyInfo)
                if int(chromenum) == 1:
                    option.add_argument(self.cf.get_conf_data(CONF_BRO_CONF)[CONF_CHRO_PATH_NAME])
                elif int(chromenum) == 2:
                    option.add_argument(self.cf.get_conf_data(CONF_BRO_CONF)[CONF_CHRO_PATH_NAME] + " - 1")
                f = self.cf.get_conf_data(CONF_BRO_CONF)[CONF_CHRO_ISDISPLAY]
                option.add_experimental_option('excludeSwitches', ['enable-automation'])
                if f == "1":
                    self.lg.info("显示Chrome浏览器界面")
                elif f == "0":
                    option.add_argument('--headless')
                    option.add_argument('--no-sandbox')
                    option.add_argument('--disable-dev-shm-usage')
                    self.lg.info("无界面启动Chrome浏览器")

                driver = Chrome(options=option)
                return driver
                # elif int(chromenum)==2:
                #     option = webdriver.ChromeOptions()
                #     option.add_argument(self.cf.get_conf_data(CONF_BRO_CONF)[CONF_CHRO_PATH_NAME]+" - 1")
                #     f = self.cf.get_conf_data(CONF_BRO_CONF)[CONF_CHRO_ISDISPLAY]
                #     if f == "1":
                #         self.lg.info("显示Chrome浏览器界面")
                #     elif f == "0":
                #         option.add_argument('--headless')
                #         option.add_argument('--no-sandbox')
                #         option.add_argument('--disable-dev-shm-usage')
                #         self.lg.info("无界面启动Chrome浏览器")
                #
                #     driver = webdriver.Chrome(options=option)
                #     return driver


            else:
                self.lg.error("未安装浏览器driver！")

        except Exception as e:
            self.lg.error(e)


class Web():
    def __init__(self, driver):
        CONF_NAME_SCRPATH = "ScreenShotPath"
        CONF_NAME_PATH = "path"
        self.lg = logoutput.Logger()
        self.driver = driver
        cf = conf.Conf()
        self.SCR_PATH = cf.get_conf_data(CONF_NAME_SCRPATH)[CONF_NAME_PATH]

    def get_element(self, elementinfo, waittime=1):
        '''
        获取元素对象，传入元素信息返回元素
        :param elementinfo:
        :param waittime:
        :return:
        '''
        time.sleep(waittime)
        try:
            element = self.driver.find_element(elementinfo["type"], elementinfo["value"])
            if element == None:
                self.lg.info("定位元素失败:%s" % elementinfo["desc"])
                self.driver.quit()
            else:
                return element
            # for i in range(60):
            #     if i>=59:
            #         self.lg.error("定位元素超时：%s"%elementinfo["desc"])
            #     try:
            #         if self.driver.find_element(elementinfo["type"], elementinfo["value"]):
            #             return self.driver.find_element(elementinfo["type"], elementinfo["value"])
            #     except:
            #         self.lg.error("未找到元素：%s"%elementinfo["desc"])
        except Exception as e:
            self.lg.error(e)
            self.lg.error("未定位到元素:%s" % elementinfo["desc"])
            self.get_screenshot()

    def wait_element(self, elementinfo, waittime=8):
        '''
        等待元素出现
        :param elementinfo:
        :param waittime:
        :return:
        '''
        # self.get_element(elementinfo)
        try:
            WebDriverWait(self.driver, waittime).until(
                lambda x: x.find_element(elementinfo["type"], elementinfo["value"]))
            self.lg.info("元素出现：%s" % elementinfo["desc"])
            return True
        except Exception as e:
            self.lg.error(e)
            self.lg.error("元素未出现：%s" % elementinfo["desc"])
            self.get_screenshot()
            return False

    def click(self, elementinfo, waittime=1):
        '''
        点击操作
        :param elementinfo:
        :return:
        '''
        e = self.get_element(elementinfo, waittime)
        try:
            e.click()
            self.lg.info("点击：%s" % elementinfo["desc"])
        except Exception as e:
            self.lg.error(e)
            self.lg.error("未点击成功：%s" % elementinfo["desc"])
            self.get_screenshot()

    def get_elements(self, elementinfo, waittime=1):
        '''
        定位一组对象
        :param elementinfo:
        :param waittime:
        :return:
        '''
        time.sleep(waittime)
        try:
            element = self.driver.find_elements(elementinfo["type"], elementinfo["value"])
            if element == None:
                self.lg.info("定位元素失败:%s" % elementinfo["desc"])
                self.driver.quit()
            else:
                return element
        except Exception as e:
            self.lg.error(e)
            self.lg.error("未定位到元素:%s" % elementinfo["desc"])
            self.get_screenshot()

    def get_screenshot(self):
        '''
        获取截图
        :return:
        '''
        try:
            t = tool.Time()
            picNam = t.get_now_time() + ".png"
            self.lg.info("保存图片：%s" % picNam)
            os.chdir(self.SCR_PATH)
            self.driver.save_screenshot(picNam)
            # f = open(picNam,'rb').read()
            self.lg.info(self.SCR_PATH + '\\' + picNam)
            allure.attach.file(self.SCR_PATH + '\\' + picNam, attachment_type=allure.attachment_type.PNG)
            # imgBase = self.driver.get_screenshot_as_base64()
            # allure.attach('<head></head><body> <img src=\"{bs}\" /> </body>'.format(bs=imgBase),
            # 'Attach with HTML type', allure.attachment_type.HTML)
        except Exception as e:
            self.lg.error(e)
            self.lg.error("获取截图失败！")

    def get_full_screenshot(self):
        '''
        获取全屏截图
        :return:
        '''
        try:
            t = tool.Time()
            picNam = t.get_now_time() + ".png"
            self.lg.info("保存图片：%s" % picNam)
            os.chdir(self.SCR_PATH)
            scroll_width = self.driver.execute_script('return document.body.parentNode.scrollWidth')
            scroll_height = self.driver.execute_script('return document.body.parentNode.scrollHeight')
            self.driver.set_window_size(scroll_width, scroll_height)
            self.driver.save_screenshot(picNam)
            # imgBase=self.driver.get_screenshot_as_base64()
            # f = open(picNam,'rb').read()
            self.lg.info(self.SCR_PATH + '\\' + picNam)
            allure.attach.file(self.SCR_PATH + '\\' + picNam, attachment_type=allure.attachment_type.PNG)
            # allure.attach('<head></head><body> <img src=\"{bs}\" /> </body>'.format(bs=imgBase), 'Attach with HTML type', allure.attachment_type.HTML)
        except Exception as e:
            self.lg.error(e)
            self.lg.error("获取截图失败！")

    def send_keys(self, elmentinfo, data):
        '''
        输入内容
        :param elmentinfo:
        :param data:
        :return:
        '''

        try:
            self.lg.info("输入内容：%s" % data)
            self.get_element(elmentinfo).send_keys(data)
        except Exception as e:
            self.lg.error(e)
            self.lg.error("输入内容失败！")

    def get_url(self, url):
        '''
        获取当前页面的url
        :param url:
        :return:
        '''
        try:
            self.driver.set_page_load_timeout(time_to_wait=30)
            self.lg.info("打开url:%s" % url)
            self.driver.get(url)
        except Exception as e:
            self.lg.error(e)
            self.lg.error("打开url失败！")
            self.get_screenshot()

    def get_text(self, elementinfo, waittime=1):
        '''
        获取页面的值
        '''
        try:
            self.lg.info("获取：“{}”的值".format(elementinfo["desc"]))
            return self.get_element(elementinfo, waittime).text

        except Exception as e:
            self.lg.error(e)
            self.lg.error("未获取到：“{}”的值".format(elementinfo["desc"]))

    def get_attribute(self, elementinfo, attribute, waittime=1):
        '''

        :param elementinfo:
        :param waittime:
        :param attribute:
        :return:
        '''
        try:
            self.lg.info("获取：“{}”的属性值".format(elementinfo["desc"]))
            return self.get_element(elementinfo, waittime).get_attribute(attribute)
        except Ellipsis as e:
            self.lg.error("未获取到：“{}”的属性值".format(elementinfo["desc"]))

    def scroll_page(self, pagesize="bottom"):
        '''
        滚动页面
        默认滚动到最底部，可以填写滚动距离数字
        :return:
        '''
        if pagesize == "bottom":

            try:
                self.lg.info("滚动页面")
                # js="var q=document.documentElement.scrollTpo=1000"
                js = " window.scrollTo(0,document.body.scrollHeight)"
                self.driver.execute_script(js)
            except Ellipsis as e:
                self.lg.error("滚动页面失败")
        else:
            try:
                self.lg.info("滚动页面")
                js = "var q=document.documentElement.scrollTpo=" + str(pagesize)
                # js = " window.scrollTo(0,document.body.scrollHeight)"
                self.driver.execute_script(js)
            except Ellipsis as e:
                self.lg.error("滚动页面失败")

    def get_page_source(self):
        '''
        获取整个页面所有内容
        :return:
        '''
        try:
            self.lg.info("获取页面信息")
            return self.driver.page_source
        except Ellipsis as e:
            self.lg.error(e)

    def is_exist(self, elementinfo, waittime=1):
        '''
        判断元素是否存在，存在返回True，不存在返回False
        :param elementinfo:
        :param waittime:
        :return:
        '''

        try:
            time.sleep(waittime)
            q = self.driver.find_element(elementinfo["type"], elementinfo["value"])
            self.lg.info("“{}”元素存在".format(elementinfo["desc"]))
            return True
        except:
            self.lg.info("“{}”元素不存在".format(elementinfo["desc"]))
            return False

    def maximize_window(self):

        '''
        窗口最大化
        :return:
        '''
        self.lg.info("最大化窗口")
        return self.driver.maximize_window()

    def move_to_element(self, elementinfo, waittime=1):
        '''
        鼠标移动到某个元素
        :param elementionf:
        :param waittime:
        :return:
        '''

        time.sleep(waittime)
        dr=self.driver.find_element(elementinfo["type"], elementinfo["value"])
        ActionChains(self.driver).move_to_element(dr).perform()

