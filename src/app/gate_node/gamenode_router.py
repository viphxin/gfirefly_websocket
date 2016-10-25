#coding:utf8
import binascii
from app.common.utils import selectTypeNode
# from gfirefly.server.globalobject import GlobalObject
from gfirefly.utils.singleton import Singleton

class GameNodeRouterException(Exception):pass

class GameNodeRouter(object):
    """
    这是一个无状态的router(算法决定)
    """
    __metaclass__ = Singleton

    def __init__(self):
        self.gamenodes = selectTypeNode("game")
        self.n = len(self.gamenodes)

    def get_node(self, identity):
        """
        获取节点
        :return:
        """
        vnode = self.get_vnode(identity)
        #这里的规则是每个物理节点平均分配玩家
        p = 1024/self.n
        for i in range(self.n, 0, -1):
            if vnode >= p*(i - 1):
                return self.gamenodes[i-1]

        raise GameNodeRouterException("GameNodeRouter get_node error. vnode %s" % vnode)


    def get_vnode(self, identity):
        """
        获取虚拟节点
        :return: 0-1023
        """
        return binascii.crc32(identity) % 1024


