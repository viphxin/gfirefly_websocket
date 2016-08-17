#coding:utf8
#import 数据库 ---start

#import 数据库 ---end
from gfirefly.server.logobj import log
from gfirefly.server.globalobject import GlobalObject
from gevent.lock import Semaphore
from app.common.utils import getOneRootByType

class Player(object):
    """
    用户
    """
    def __init__(self, pid, sessionno):
        """
        初始化玩家信息(加载玩家相关数据到内存)
        :param uid:
        :param sessionno:
        :return:
        """
        self.pid = pid#玩家ID
        self.rid = None#角色ID
        self.sessionno = sessionno#玩家客户端动态ID
        self.lock = Semaphore()#玩家锁

        self.player_status = 1 #1 正常 2 离线
        #player property
        self.player_info = {}#玩家信息
        self.bag_info = {}#背包信息
        self.fuwen_info = None#符文信息
        self.pifu_info = {}#皮肤信息
        self.propertybag = {}#客户端自定义属性
        #sys property
        self.lastaction = None #最后操作
        self.lastactiontime = None #最后操作时间
        self.initDataFromDb()

    def reconnection(self, sessionno):
        """
        断线重连处理
        :param sessionno:
        :return:
        """
        #更新客户端net动态ID
        self.sessionno = sessionno

    def setOffline(self):
        """
        设置玩家离线
        :return:
        """
        self.player_status = 2

    def initDataFromDb(self):
        """
        加载数据
        :return:
        """
        log.msg("init data %s" % self.pid)


    def saveDataToDb(self):
        """
        持久化用户数据
        :return:
        """
        log.msg("saveDataToDb %s" % self.pid)


    def sendMsg(self, data):
        """
        客户端推送消息
        :param data:
        :return:
        """
        getOneRootByType("gate").callRemoteNotForResult("sendMsg", data, [self.sessionno])