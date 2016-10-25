#coding:utf8
from gevent.queue import Queue
from gfirefly.server.globalobject import GlobalObject

class Player(object):
    """
    房间内的玩家
    """
    def __init__(self, conn, rid):
        """
        :param conn: 客户端链接
        :param rid: 房间内唯一ID
        :return:
        """
        self.conn = conn
        self.rid = rid
        self.propertyBag = {}#保存玩家属性
        self.msgQueue = Queue()#消息队列缓存，用于断线后游戏回放

        self.player_state = 0 #0 队列中 1 已确认(准备) 2 房间中 3 资源加载完 4 end

    @property
    def sid(self):
        """
        客户端动态唯一ID
        :return:
        """
        return self.conn.transport.sessionno if self.conn else None

    @property
    def uid(self):
        """
        客户端玩家ID
        :return:
        """
        return getattr(self.conn, "uid", None)

    @property
    def isOnline(self):
        """
        是否在线
        :return:
        """
        return False if self.sid is None else True

    def setState(self, s):
        """
        设置玩家状态
        :param s:
        :return:
        """
        self.player_state = s

    @property
    def playerState(self):
        return self.player_state

    def sendMsg(self, commandId, data):
        """
        发送消息给客户端
        :param commandId: 操作码
        :param data: 数据
        :return:
        """
        if self.conn:
            self.conn.safeToWriteData(data, commandId)
        else:
            #掉线了, 缓存数据
            self.msgQueue.put_nowait((commandId, data))

    def addProperty(self, k, v):
        """
        添加属性
        :param k:
        :param v:
        :return:
        """
        self.propertyBag[k] = v

    def removeProperty(self, k):
        """
        移除属性
        :param k:
        :return:
        """
        del self.propertyBag[k]

    def getProperty(self, k):
        """
        获取属性
        :param k:
        :return:
        """
        return self.propertyBag.get(k, None)

    def lostConnection(self):
        """
        断线
        :return:
        """
        self.conn = None

    def reConnection(self, conn):
        """
        断线重连
        :param conn:
        :return:
        """
        self.conn = conn