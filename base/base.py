# coding=utf-8
from appium import webdriver as appwebdriver
from common import conf
from common import tool
from common import logoutput
import time
import os
from selenium.webdriver.support.ui import WebDriverWait
from selenium import webdriver
import allure


class SetUp():
    '''
    appbase中setup类，用来启动app，返回一个driver对象
    '''

    def __init__(self):
        # self.CONF_PATH = CONF_PATH
        self.lg=logoutput.Logger()
    def app_setup(self):
        CONF_NAME_DEVICEINFO="DeviceInfo"
        CONF_NAME_REMOTE="remote"
        CONF_NAME_ADDR="addr"
        '''
        启动app，从配置文件中获取机型信息，remote的地址ixnxi
        :param deviceinfo:
        :return:
        '''
        # path = self.CONF_PATH
        try:
            cf = conf.Conf()
            info = cf.get_conf_data(CONF_NAME_DEVICEINFO)
            self.lg.info("读取机型信息：%s" % info)
            driver = appwebdriver.Remote(cf.get_conf_data(CONF_NAME_REMOTE)[CONF_NAME_ADDR], info)
            self.lg.info("读取remote信息：%s" % cf.get_conf_data(CONF_NAME_REMOTE)[CONF_NAME_ADDR])
            return driver
        except Exception as e:
            self.lg.war(e)
            self.lg.error("启动app失败!")

    def web_setup(self):
        try:
            driver=webdriver.Firefox()
            return driver
        except Exception as e:
            self.lg.error(e)


class App():
    '''
    appbase类
    '''

    def __init__(self, driver, path):
        CONF_NAME_SCRPATH="ScreenShotPath"
        CONF_NAME_PATH="path"
        self.lg=logoutput.Logger()
        '''
        传入driver对象
        :param driver:
        :return:
        '''
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
        except Exception as e:
            self.lg.error(e)
            self.lg.error("未定位到元素:%s" % elementinfo["desc"])

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
        except Exception as e:
            self.lg.error(e)
            self.lg.error("元素未出现：%s" % elementinfo["desc"])

    def click(self, elementinfo):
        '''
        点击操作
        :param elementinfo:
        :return:
        '''
        e = self.get_element(elementinfo)
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
            picNam = t.get_now_time() + ".jpg"
            self.lg.info("保存图片：%s" % picNam)
            os.chdir(self.SCR_PATH)
            self.driver.save_screenshot(picNam)
            f = open(picNam,'rb').read()
            allure.attach('This is a picture',f,allure.attach_type.PNG)
        except Exception as e:
            self.lg.error(e)
            self.lg.error("获取截图失败！")

    def install_app(self, path):
        '''
        安装app，传入
        :param path:
        :return:
        '''
        try:
            self.lg.info("安卓app...")
            self.driver.install_app(path)
        except Exception as e:
            self.lg.error(e)
            self.lg.error("安装app失败")

    def uninstall_app(self, appid):
        '''
        卸载app，传入包名
        :param appid:
        :return:
        '''
        try:
            self.driver.remove_app(appid)
        except Exception as e:
            self.lg.error(e)
            self.lg.error("卸载app失败！")

    def is_install(self, appid):
        '''
        app已安装返回True 否则返回False
        :param appid:
        :return:
        '''
        try:
            return self.driver.is_app_installed(appid)
        except Exception as e:
            self.lg.error(e)
            self.lg.error("无法确定app是否安装")

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


class Web():
    def __init__(self, path, driver):
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
        except Exception as e:
            self.lg.error(e)
            self.lg.error("未定位到元素:%s" % elementinfo["desc"])

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
        except Exception as e:
            self.lg.error(e)
            self.lg.error("元素未出现：%s" % elementinfo["desc"])

    def click(self, elementinfo):
        '''
        点击操作
        :param elementinfo:
        :return:
        '''
        e = self.get_element(elementinfo)
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
            picNam = t.get_now_time() + ".jpg"
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
        try:
            self.lg.info("打开url%s"%url)
            self.driver.get(url)
        except Exception as e:
            self.lg.error(e)
            self.lg.error("打开url失败！")
# s=SetUp(r"../test.conf")
# driver=s.app_setup()
# a=App(driver,"../test.conf")
# info={"type":"id","value":"com.fxphone:id/activity_main_course","desc":"课程"}
# time.sleep(10)
# # driver.find_element_by_id("com.fxphone:id/activity_main_course").click()
# print(a.is_install("com.fxphone"))
# a.wait_element(info)
# a.click(info)
# # driver.quit()
