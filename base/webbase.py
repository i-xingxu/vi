# coding=utf-8
from common import conf
from common import tool
from common import logoutput
import time
import os
from selenium.webdriver.support.ui import WebDriverWait
from selenium import webdriver
import allure
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary

class SetUp():
    '''
    appbase中setup类，用来启动app，返回一个driver对象
    '''

    def __init__(self):
        # self.CONF_PATH = CONF_PATH
        self.lg=logoutput.Logger()
        self.cf = conf.Conf()

    def web_setup(self):
        # """
        # 通过配置文件的的配置来控制使用哪个浏览器
        # 配置文件示例：
        # [BrowserPath]
        #     path=E:\Program Files\Mozilla Firefox\firefox.exe
        #     profile= C:\Users\xingxu\AppData\Roaming\Mozilla\Firefox\Profiles\2okoudy8.default
        #     chromprofile=--user-data-dir=C:\Users\xingxu\AppData\Local\Google\Chrome\User Data\
        # [Browser]
        #     browser=Chrome
        #
        # CONF_BRO_PATH：浏览器路径
        # CONF_FIR_PATH_NAME：火狐路径
        # CONF_FIR_PROFILE：火狐浏览器个人配置文件路径
        # CONF_BROWSER：浏览器类型
        # CONF_BRO_TYPE：浏览器类型项
        # CONF_CHRO_PATH_NAME：Chrome浏览器个人配置文件路径
        #
        # :return:
        # """

        try:
            CONF_BRO_CONF="BrowserConfig"
            CONF_FIR_PATH_NAME="firefoxpath"
            CONF_FIR_PROFILE="firefoxprofile"
            CONF_BROWSER="Browser"
            CONF_BRO_TYPE="browser"
            CONF_CHRO_PATH_NAME="chromprofile"
            CONF_CHRO_ISDISPLAY="chromeisdisplay"

            browserType=self.cf.get_conf_data(CONF_BROWSER)[CONF_BRO_TYPE]
            if browserType=="Firefox":
                binary = FirefoxBinary(self.cf.get_conf_data(CONF_BRO_CONF)[CONF_FIR_PATH_NAME])
                fp=webdriver.FirefoxProfile(self.cf.get_conf_data(CONF_BRO_CONF)[CONF_FIR_PROFILE])
                driver=webdriver.Firefox(firefox_binary=binary,firefox_profile=fp)
                return driver
            elif browserType=="Chrome":
                option = webdriver.ChromeOptions()
                option.add_argument(self.cf.get_conf_data(CONF_BRO_CONF)[CONF_CHRO_PATH_NAME])
                f=self.cf.get_conf_data(CONF_BRO_CONF)[CONF_CHRO_ISDISPLAY]
                if f=="1":
                    self.lg.info("显示Chrome浏览器界面")
                elif f=="0":
                    option.add_argument('--headless')
                    option.add_argument('--no-sandbox')
                    option.add_argument('--disable-dev-shm-usage')
                    self.lg.info("无界面启动Chrome浏览器")

                driver=webdriver.Chrome(chrome_options=option)
                return driver
            else:
                self.lg.error("未安装浏览器driver！")

        except Exception as e:
            self.lg.error(e)
class Web():
    def __init__(self,driver):
        CONF_NAME_SCRPATH="ScreenShotPath"
        CONF_NAME_PATH="path"
        self.lg=logoutput.Logger()
        self.driver = driver
        cf=conf.Conf()
        self.SCR_PATH = cf.get_conf_data( CONF_NAME_SCRPATH)[CONF_NAME_PATH]

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
        self.get_element(elementinfo)
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

    def click(self, elementinfo,waittime=1):
        '''
        点击操作
        :param elementinfo:
        :return:
        '''
        e = self.get_element(elementinfo,waittime)
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
            f = open(picNam,'rb').read()
            allure.attach('This is a picture',f,allure.attach_type.PNG)
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
    def get_url(self,url):
        '''
        获取当前页面的url
        :param url:
        :return:
        '''
        try:
            self.driver.set_page_load_timeout(time_to_wait=30)
            self.lg.info("打开url:%s"%url)
            self.driver.get(url)
        except Exception as e:
            self.lg.error(e)
            self.lg.error("打开url失败！")
            self.get_screenshot()

    def get_text(self,elementinfo,waittime=1):
        '''
        获取页面的值
        '''
        try:
            self.lg.info("获取：“{}”的值".format(elementinfo["desc"]))
            return self.get_element(elementinfo,waittime).text

        except Exception as e:
            self.lg.error(e)
            self.lg.error("未获取到：“{}”的值".format(elementinfo["desc"]))


    def get_attribute(self,elementinfo,attribute,waittime=1):
        '''

        :param elementinfo:
        :param waittime:
        :param attribute:
        :return:
        '''
        try:
            self.lg.info("获取：“{}”的属性值".format(elementinfo["desc"]))
            return  self.get_element(elementinfo,waittime).get_attribute(attribute)
        except Ellipsis as e:
            self.lg.error("未获取到：“{}”的属性值".format(elementinfo["desc"]))

    def scroll_page(self,pagesize="bottom"):
        '''
        滚动页面
        默认滚动到最底部，可以填写滚动距离数字
        :return:
        '''
        if pagesize=="bottom":

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
                js="var q=document.documentElement.scrollTpo="+str(pagesize)
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
            return  self.driver.page_source
        except Ellipsis as e:
            self.lg.error(e)

    def is_exist(self,elementinfo,waittime=1):
        '''
        判断元素是否存在，存在返回True，不存在返回False
        :param elementinfo:
        :param waittime:
        :return:
        '''

        try:
            time.sleep(waittime)
            q=self.driver.find_element(elementinfo["type"], elementinfo["value"])
            self.lg.info("“{}”元素存在".format(elementinfo["desc"]))
            return  True
        except:
            self.lg.info("“{}”元素不存在".format(elementinfo["desc"]))
            return False


