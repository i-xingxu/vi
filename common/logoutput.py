# coding = utf-8
import logging,os
from common import tool,conf


class Logger():
    '''
    日志输出
    '''
    def __init__(self,clevel = logging.DEBUG,Flevel = logging.DEBUG):
        CONF_NAME_LOGPATH="LogPath"
        CONF_NAME_PATHINFO="LogPath"
        '''
        :param clevel:
        :param Flevel:
        :return:
        '''
        try:
            cf=conf.Conf()
            c=cf.get_conf_data(CONF_NAME_LOGPATH)
            os.chdir(c[CONF_NAME_PATHINFO])
            t=tool.Time()
            date=t.get_now_time().split(" ")[0]
            self.logger = logging.getLogger(date+".log")
            self.logger.setLevel(logging.DEBUG)
            fmt = logging.Formatter('[%(asctime)s] [%(levelname)s] %(message)s', '%Y-%m-%d %H:%M:%S')
            if not self.logger.handlers:
                #设置CMD日志
                sh = logging.StreamHandler()
                sh.setFormatter(fmt)
                sh.setLevel(clevel)
                #设置文件日志
                fh = logging.FileHandler(date+".log",encoding='utf-8')
                fh.setFormatter(fmt)
                fh.setLevel(Flevel)
                self.logger.addHandler(sh)
                self.logger.addHandler(fh)
        except Exception as e:
            print(e)


    def debug(self,message):
        self.logger.debug(message)


    def info(self,message):
        self.logger.info(message)


    def war(self,message):
      self.logger.warn(message)


    def error(self,message):
      self.logger.error(message)


    def cri(self,message):
      self.logger.critical(message)
